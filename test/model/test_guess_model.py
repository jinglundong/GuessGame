import unittest
from datetime import datetime
from datetime import timedelta

from google.appengine.ext import ndb
from google.appengine.api import memcache
from google.appengine.ext import testbed

from service.model.guess import Guess 

class TestGuess(unittest.TestCase):
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

    def test_list_all_guesses_from_same_game(self):
        GAME_ID = 'ID1'
        guess1_game1 = Guess(
            game_id = GAME_ID,
            user_id = 'UserId',
            guess_num = '1234',
            aligned = 2,
            not_aligned = 2)
        guess1_game1.put()

        guess2_game1 = Guess(
            game_id = GAME_ID,
            user_id = 'UserId',
            guess_num = '4321',
            aligned = 2,
            not_aligned = 2)
        guess2_game1.put()

        guesses = Guess.list_all_guess_of_a_game(GAME_ID)
 
        self.assertEqual(2, len(guesses))

    def test_list_identical_guesses_from_same_game(self):
        GAME_ID = 'ID1'
        guess1_game1 = Guess(
            game_id = GAME_ID,
            user_id = 'UserId',
            guess_num = '1234',
            aligned = 2,
            not_aligned = 2)
        guess1_game1.put()

        guess2_game1 = Guess(
            game_id = GAME_ID,
            user_id = 'UserId',
            guess_num = '1234',
            aligned = 2,
            not_aligned = 2)
        guess2_game1.put()

        guesses = Guess.list_all_guess_of_a_game(GAME_ID)
 
        self.assertEqual(2, len(guesses))

    def test_list_all_guess_of_a_game(self):
        guess1_game1 = Guess(
            game_id = 'ID1',
            user_id = 'UserId',
            guess_num = '1234',
            aligned = 2,
            not_aligned = 2)
        guess1_game1.put()

        guess2_game1 = Guess(
            game_id = 'ID1',
            user_id = 'UserId',
            guess_num = '2222',
            aligned = 2,
            not_aligned = 2)
        guess2_game1.put()

        guess1_game2 = Guess(
            game_id = 'ID2',
            user_id = 'UserId',
            guess_num = '1234',
            aligned = 2,
            not_aligned = 2)
        guess1_game2.put()

        guesses = Guess.list_all_guess_of_a_game('ID1')

        self.assertEqual(2, len(guesses))
