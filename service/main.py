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
import random
import math

from google.appengine.api import users
from service.model.game import Game


class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
            greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(
                nickname, logout_url)
        else:
            login_url = users.create_login_url('/')
            greeting = '<a href="{}">Sign in</a>'.format(login_url)

        self.response.write(
            '<html><body>{}</body></html>'.format(greeting))

class SecondPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')

class GameListPage(webapp2.RequestHandler):
    def get(self):
        games = Game.list_all_games_from_new_to_old()
        game_list = ""
 
        for game in games:
            game_list += game.game_id
            game_list += '</br>'

        self.response.write(
            '<html><body>{}</body></html>'.format(game_list))

class CreateGame(webapp2.RequestHandler):
    def post(self):
        game_id = str(int(math.floor(random.random() * 10000000)))
        answer = str(int(math.floor(random.random() * 1000)))

        Game.new_game(game_id, answer)


app = webapp2.WSGIApplication([
    ('/second', SecondPage),
    ('/', MainPage),
    ('/games', GameListPage),
    ('/new_game', CreateGame)
 
], debug=True)
