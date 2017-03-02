from google.appengine.ext import ndb

class Guess(ndb.Model):
    """Models a single Guess operation of a Guess Game."""

    game_id = ndb.StringProperty()
    user_id = ndb.StringProperty()
    guess_num = ndb.StringProperty()
    aligned = ndb.IntegerProperty()
    not_aligned = ndb.IntegerProperty() 
    date = ndb.DateTimeProperty(auto_now_add=True)
 
    @classmethod
    def list_all_guess_of_a_game(cls, game_id):
        return Guess.query(Guess.game_id == game_id).fetch()

