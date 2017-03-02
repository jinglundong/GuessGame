from google.appengine.ext import ndb

class Game(ndb.Model):
    """Models a single Guess Game."""

    game_id = ndb.StringProperty()
    answer = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    is_solved = ndb.BooleanProperty(default=False)

    @classmethod
    def query_game(cls, game_id):
        return Game.query(Game.game_id == game_id).fetch()

    @classmethod
    def list_all_games_from_new_to_old(cls):
        return Game.query().order(-Game.date).fetch()

    @classmethod
    def guess(cls, game_id, guessNum):
        games = Game.query(Game.game_id == game_id).fetch()

        if games:
            game = games[0]

        if guessNum == game.answer:
            game.is_solved = True
            game.put()
            return True
        else:
            return False

    @classmethod
    def new_game(cls, game_id, answer):
        game = Game(
            game_id = game_id, answer = answer)
        game.put()
