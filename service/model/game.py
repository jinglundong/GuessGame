from google.appengine.ext import ndb

class Game(ndb.Model):
    """Models a single Guess Game."""

    game_id = ndb.StringProperty()
    answer = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def query_game(cls, game_id):
        return cls.query(ancestor = game_id).fetch()