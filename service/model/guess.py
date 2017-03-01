from google.appengine.ext import ndb

class Guess(ndb.Model):
    """Models a single Guess operation of a Guess Game."""

    game_id = ndb.StringProperty()
    user_id = ndb.StringProperty()
    guess_num = ndb.StringProperty()
    aligned = ndb.IntegerProperty()
    not_aligned = ndb.IntegerProperty() 
    date = ndb.DateTimeProperty(auto_now_add=True)
