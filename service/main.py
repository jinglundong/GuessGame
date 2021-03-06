# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import jinja2
import random
import math
import os
import time

from google.appengine.api import users

from service.model.game import Game
from service.model.guess import Guess
from service.indicator import Indicator

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class GameListPage(webapp2.RequestHandler):
    def get(self):
        games = Game.list_all_unsolved_games_from_new_to_old()

        template_values = {
            'games': games
        }

        template = JINJA_ENVIRONMENT.get_template('view/index.html')
        self.response.write(template.render(template_values))

class CreateGame(webapp2.RequestHandler):
    def post(self):
        game_id = str(int(math.floor(random.random() * 10000000)))
        answer = str(int(math.floor(random.random() * 10000)))

        Game.new_game(game_id, answer)
        for retry in range(3):
            if Game.query_game(game_id):
                return webapp2.redirect('/game?game_id=' + game_id)
            else:
                time.sleep(0.5)
        raise Exception("Couldn't read newly created game from data store.")

class MakeGuess(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()

        game_id = self.request.get('game_id')
        guess_num = self.request.get('guess')

        game = Game.query_game(game_id)[0]
        answer = game.answer

        indicator = Indicator()
        aligned, not_aligned = indicator.indicate(guess_num, answer)

        guesses = Guess.list_all_guess_of_a_game(game_id)

        guess = Guess(
                    game_id = game_id,
                    user_id = user.nickname(),
                    guess_num = str(guess_num),
                    aligned = aligned,
                    not_aligned = not_aligned)

        if not game.is_solved:
          guess.put()
          guesses.insert(0, guess)

        guesses.reverse()

        if aligned == 4:
            self.mark_solved(game)

        template_values = {
            'guesses': guesses,
            'game_id': game_id,
            'is_solved': game.is_solved
        }

        template = JINJA_ENVIRONMENT.get_template('view/guess_ajax.html')
        self.response.write(template.render(template_values))

    def mark_solved(self, game):
        game.is_solved = True
        game.put()

class ListGuesses(webapp2.RequestHandler):
    def get(self):
        game_id = self.request.get('game_id')

        game = Game.query_game(game_id)[0]

        guesses = Guess.list_all_guess_of_a_game(game_id)
        guesses.reverse()

        template_values = {
            'guesses': guesses,
            'game_id': game_id,
            'is_solved' : game.is_solved
        }

        template = JINJA_ENVIRONMENT.get_template('view/game.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', GameListPage),
    ('/games', GameListPage),
    ('/new_game', CreateGame),
    ('/guess', MakeGuess),
    ('/game', ListGuesses)

 
], debug=True)
