import unittest
from datetime import datetime
from datetime import timedelta

from google.appengine.ext import ndb
from google.appengine.api import memcache
from google.appengine.ext import testbed

from service.model.guess import Guess 

class TestGame(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()

    def test_read_after_write(self):
        test_guess = Guess(
            game_id = 'ID',
            user_id = 'UserId',
            guess_num = '1234',
            aligned = 2,
            not_aligned = 2)
        test_guess_key = test_guess.put()

        guess = test_guess_key.get()

        self.assertEqual('ID', guess.game_id)
        self.assertEqual('UserId', guess.user_id)
        self.assertEqual('1234', guess.guess_num)
        self.assertEqual(2, guess.aligned)
        self.assertEqual(2, guess.not_aligned)
