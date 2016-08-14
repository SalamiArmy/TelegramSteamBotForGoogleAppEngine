import unittest
from gcloud import datastore


class TestGetTrending(unittest.TestCase):
    def test_gettrending(self):
        client = datastore.Client()
        product_key = client.key('Product', 123)
        print(client.get(product_key))