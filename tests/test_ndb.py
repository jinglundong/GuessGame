import unittest
import cgi
import os
from google.appengine.ext import ndb
from google.appengine.api import memcache
from google.appengine.ext import testbed

class Account(ndb.Model):
    username = ndb.StringProperty()
    userid = ndb.IntegerProperty()
    email = ndb.StringProperty()

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()

    def test_read_after_write(self):
        sandy = Account(
            username='Sandy', userid=123, email='sandy@example.com')
        sandy_key = sandy.put() 

        sandy = sandy_key.get()
        self.assertEqual('Sandy', sandy.username)
