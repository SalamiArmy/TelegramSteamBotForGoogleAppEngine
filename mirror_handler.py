import os
import re
import urllib
import urlparse
import hashlib

import logging

from google.appengine.api import memcache
from google.appengine.api import urlfetch
from google.appengine.runtime import apiproxy_errors

import webapp2

# URLs that have absolute addresses
ABSOLUTE_URL_REGEX = r"(http(s?):)?//(?P<url>[^\"'> \t\)]+)"

# URLs that are relative to the base of the current hostname.
BASE_RELATIVE_URL_REGEX = r"/(?!(/)|(http(s?)://)|(url\())(?P<url>[^\"'> \t\)]*)"

# URLs that have '../' or './' to start off their paths.
TRAVERSAL_URL_REGEX = r"(?P<relative>\.(\.)?)/(?!(/)|(http(s?)://)|(url\())(?P<url>[^\"'> \t\)]*)"

# URLs that are in the same directory as the requested URL.
SAME_DIR_URL_REGEX = r"(?!(/)|(http(s?)://)|(url\())(?P<url>[^\"'> \t\)]+)"

# URL matches the root directory.
ROOT_DIR_URL_REGEX = r"(?!//(?!>))/(?P<url>)(?=[ \t\n]*[\"'\)>/])"

# Start of a tag using 'src' or 'href'
TAG_START = r"(?i)\b(?P<tag>src|href|action|url|background)(?P<equals>[\t ]*=[\t ]*)(?P<quote>[\"']?)"

# Start of a CSS import
CSS_IMPORT_START = r"(?i)@import(?P<spacing>[\t ]+)(?P<quote>[\"']?)"

# CSS url() call
CSS_URL_START = r"(?i)\burl\((?P<quote>[\"']?)"


REPLACEMENT_REGEXES = [
  (TAG_START + SAME_DIR_URL_REGEX,
     "\g<tag>\g<equals>\g<quote>%(accessed_dir)s\g<url>"),

  (TAG_START + TRAVERSAL_URL_REGEX,
     "\g<tag>\g<equals>\g<quote>%(accessed_dir)s/\g<relative>/\g<url>"),

  (TAG_START + BASE_RELATIVE_URL_REGEX,
     "\g<tag>\g<equals>\g<quote>/%(base)s/\g<url>"),

  (TAG_START + ROOT_DIR_URL_REGEX,
     "\g<tag>\g<equals>\g<quote>/%(base)s/"),

  # Need this because HTML tags could end with '/>', which confuses the
  # tag-matching regex above, since that's the end-of-match signal.
  (TAG_START + ABSOLUTE_URL_REGEX,
     "\g<tag>\g<equals>\g<quote>/\g<url>"),

  (CSS_IMPORT_START + SAME_DIR_URL_REGEX,
     "@import\g<spacing>\g<quote>%(accessed_dir)s\g<url>"),

  (CSS_IMPORT_START + TRAVERSAL_URL_REGEX,
     "@import\g<spacing>\g<quote>%(accessed_dir)s/\g<relative>/\g<url>"),

  (CSS_IMPORT_START + BASE_RELATIVE_URL_REGEX,
     "@import\g<spacing>\g<quote>/%(base)s/\g<url>"),

  (CSS_IMPORT_START + ABSOLUTE_URL_REGEX,
     "@import\g<spacing>\g<quote>/\g<url>"),

  (CSS_URL_START + SAME_DIR_URL_REGEX,
     "url(\g<quote>%(accessed_dir)s\g<url>"),

  (CSS_URL_START + TRAVERSAL_URL_REGEX,
      "url(\g<quote>%(accessed_dir)s/\g<relative>/\g<url>"),

  (CSS_URL_START + BASE_RELATIVE_URL_REGEX,
      "url(\g<quote>/%(base)s/\g<url>"),

  (CSS_URL_START + ABSOLUTE_URL_REGEX,
      "url(\g<quote>/\g<url>"),
]

def TransformContent(base_url, accessed_url, content):
  url_obj = urlparse.urlparse(accessed_url)
  accessed_dir = os.path.dirname(url_obj.path)
  if not accessed_dir.endswith("/"):
    accessed_dir += "/"

  for pattern, replacement in REPLACEMENT_REGEXES:
    fixed_replacement = replacement % {
      "base": base_url,
      "accessed_dir": accessed_dir,
    }
    content = re.sub(pattern, fixed_replacement, content)
  return content

DEBUG = False
EXPIRATION_DELTA_SECONDS = 3600

# DEBUG = True
# EXPIRATION_DELTA_SECONDS = 10

HTTP_PREFIX = "http://"

IGNORE_HEADERS = frozenset([
  "set-cookie",
  "expires",
  "cache-control",

  # Ignore hop-by-hop headers
  "connection",
  "keep-alive",
  "proxy-authenticate",
  "proxy-authorization",
  "te",
  "trailers",
  "transfer-encoding",
  "upgrade",
])

TRANSFORMED_CONTENT_TYPES = frozenset([
  "text/html",
  "text/css",
])

MAX_CONTENT_SIZE = 10 ** 6 - 600

def get_url_key_name(url):
  url_hash = hashlib.sha256()
  url_hash.update(url)
  return "hash_" + url_hash.hexdigest()

class MirroredContent(object):
  def __init__(self, original_address, translated_address,
               status, headers, data, base_url):
    self.original_address = original_address
    self.translated_address = translated_address
    self.status = status
    self.headers = headers
    self.data = data
    self.base_url = base_url

  @staticmethod
  def get_by_key_name(key_name):
    return memcache.get(key_name)

  @staticmethod
  def fetch_and_store(key_name, base_url, translated_address, mirrored_url, postdata=None, headers=None):
    """Fetch and cache a page.
    Args:
      key_name: Hash to use to store the cached page.
      base_url: The hostname of the page that's being mirrored.
      translated_address: The URL of the mirrored page on this site.
      mirrored_url: The URL of the original page. Hostname should match
        the base_url.
      postdata: If there is any.
    Returns:
      A new MirroredContent object, if the page was successfully retrieved.
      None if any errors occurred or the content could not be retrieved.
    """
    logging.debug("Fetching '%s'", mirrored_url)
    try:
      if postdata and headers:
        response = urlfetch.fetch(mirrored_url, urllib.urlencode(postdata), urlfetch.POST, headers)
      elif postdata:
        response = urlfetch.fetch(mirrored_url, urllib.urlencode(postdata), urlfetch.POST)
      elif headers:
        response = urlfetch.fetch(mirrored_url, urllib.urlencode(postdata), urlfetch.GET, headers)
      else:
        response = urlfetch.fetch(mirrored_url)
    except (urlfetch.Error, apiproxy_errors.Error):
      logging.exception("Could not fetch URL")
      return None

    adjusted_headers = {}
    for key, value in response.headers.iteritems():
      adjusted_key = key.lower()
      if adjusted_key not in IGNORE_HEADERS:
        adjusted_headers[adjusted_key] = value

    content = response.content
    page_content_type = adjusted_headers.get("content-type", "")
    for content_type in TRANSFORMED_CONTENT_TYPES:
      # startswith() because there could be a 'charset=UTF-8' in the header.
      if page_content_type.startswith(content_type):
        content = TransformContent(base_url, mirrored_url, content)
        break

    new_content = MirroredContent(
      base_url=base_url,
      original_address=mirrored_url,
      translated_address=translated_address,
      status=response.status_code,
      headers=adjusted_headers,
      data=content)

    # Do not memcache content over 1MB
    if len(content) < MAX_CONTENT_SIZE:
      if not memcache.add(key_name, new_content, time=EXPIRATION_DELTA_SECONDS):
        logging.error('memcache.add failed: key_name = "%s", '
                      'original_url = "%s"', key_name, mirrored_url)
    else:
      logging.warning("Content is over 1MB; not memcached")

    return new_content

class BaseHandler(webapp2.RequestHandler):
  def get_relative_url(self):
    slash = self.request.url.find("/", len(self.request.scheme + "://"))
    if slash == -1:
      return "/"
    return self.request.url[slash:]

  def is_recursive_request(self):
    if "AppEngine-Google" in self.request.headers.get("User-Agent", ""):
      logging.warning("Ignoring recursive request by user-agent=%r; ignoring")
      self.error(404)
      return True
    return False

class MirrorHandler(BaseHandler):
  def get(self, base_url):
    if self.is_recursive_request() or not base_url and \
            not base_url.EndsWith('.steampowered.com') and \
            not base_url.EndsWith('.steamstatic.com'):
      return

    # Log the user-agent and referrer, to see who is linking to us.
    logging.debug('User-Agent = "%s", Referrer = "%s"',
                  self.request.user_agent,
                  self.request.referer)
    logging.debug('Base_url = "%s", url = "%s"', base_url, self.request.url)

    translated_address = self.get_relative_url()[1:]  # remove leading /
    mirrored_url = "http://" + translated_address

    # Use sha256 hash instead of mirrored url for the key name, since key
    # names can only be 500 bytes in length; URLs may be up to 2KB.
    key_name = get_url_key_name(mirrored_url)
    logging.info("Handling request for '%s' = '%s'", mirrored_url, key_name)

    content = MirroredContent.get_by_key_name(key_name)
    cache_miss = False
    if content is None:
      logging.debug("Cache miss")
      cache_miss = True
      post_data = dict([(x,self.request.get(x)) for x in self.request.arguments()])
      content = MirroredContent.fetch_and_store(key_name, base_url, translated_address, mirrored_url, post_data, self.request.headers)
    if content is None:
      return self.error(404)

    for key, value in content.headers.iteritems():
      self.response.headers[key] = value
    if not DEBUG:
      self.response.headers["cache-control"] = \
        "max-age=%d" % EXPIRATION_DELTA_SECONDS

    self.response.out.write(content.data)

  def post(self, base_url):
      self.get(base_url)