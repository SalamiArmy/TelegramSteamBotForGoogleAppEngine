from google.appengine.ext import vendor

# Try add any libraries installed in the "lib" folder.
try:
    vendor.add('lib')
except:
    print('ImageBoet failed to add it\'s third-party libraries folder to app engine\'s vendor.')
