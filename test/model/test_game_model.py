import unittest
from datetime import datetime
from datetime import timedelta

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
            game_id = 'ID1', answer = '1234')
        test_game_key = test_game.put()

        games = Game.query_game('ID1')
        self.assertEqual(1, len(games))
        self.assertEqual('ID1', games[0].game_id)
        self.assertEqual(False, games[0].is_solved)

    def test_list_all_games_from_new_to_old(self):
        now = datetime.now()

        test_game_early = Game(
            game_id = 'ID_OLD', answer = '1234', date = now)
        test_game_early_key = test_game_early.put()

        test_game_later = Game(
            game_id = 'ID_OLD', answer = '1234', date = now + timedelta(days=1))
        test_game_later_key = test_game_later.put()

        games = Game.list_all_games_from_new_to_old()

        self.assertTrue(games[0].date - games[1].date == timedelta(days=1))

    def test_wrong_guess(self):
        test_game = Game(
            game_id = 'ID1', answer = '1234')
        test_game_key = test_game.put()

        result = Game.guess('ID1', '0000')
        self.assertFalse(result)

    def test_right_guess(self):
        test_game = Game(
            game_id = 'ID1', answer = '1234')
        test_game_key = test_game.put()

        result = Game.guess('ID1', '1234')
        self.assertTrue(result)
        self.assertTrue(Game.query_game('ID1')[0].is_solved)
