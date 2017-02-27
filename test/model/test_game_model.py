import unittest

from google.appengine.ext import ndb
from google.appengine.api import memcache
from google.appengine.ext import testbed

from service.model.game import Game

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
        test_game = Game(
            game_id = 'ID1', answer = '1234')
        test_game_key = test_game.put()

        returned_test_game = test_game_key.get()
        self.assertEqual('1234', returned_test_game.answer)

    def test_query_game(self):
        test_game = Game(
            game_id = 'ID1', answer = '1234', is_solved = False)
        test_game_key = test_game.put()

        games = Game.query_game('ID1')
        self.assertEqual(1, len(games))
        self.assertEqual('ID1', games[0].game_id)
        self.assertEqual(False, games[0].is_solved)
