import datetime
from . import db # import db instance from models/__init__.py
from marshmallow import fields, Schema
from .ResultModel import ResultSchema
from sqlalchemy import or_

class GameModel(db.Model): # GameModel class inherits from db.Model
  __tablename__ = 'games' # name our table Games

  id = db.Column(db.Integer, primary_key=True)
  organiser_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
  opponent_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
  status = db.Column(db.String, default='pending', nullable=False)
  game_date = db.Column(db.Date, nullable=False)
  game_time = db.Column(db.Time, nullable=False)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)
  sport = db.Column(db.String, nullable=True)
  venue = db.Column(db.String, nullable=True)
  winner_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=True)
  loser_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=True)
  organiser = db.relationship("PlayerModel", primaryjoin = "GameModel.organiser_id == PlayerModel.id", backref="organiser")
  opponent = db.relationship("PlayerModel", primaryjoin = "GameModel.opponent_id == PlayerModel.id", backref="opponent")
  winner = db.relationship("PlayerModel", primaryjoin = "GameModel.winner_id == PlayerModel.id", backref="winner")
  loser = db.relationship("PlayerModel", primaryjoin = "GameModel.loser_id == PlayerModel.id", backref="loser")
  result = db.relationship("ResultModel", uselist=False, back_populates="game")

  def __init__(self, data): # class constructor used to set the class attributes
    self.organiser_id = data.get('organiser_id')
    self.opponent_id = data.get('opponent_id')
    self.game_date = data.get('game_date')
    self.game_time = data.get('game_time')
    self.sport = data.get('sport')
    self.venue = data.get('venue')
    self.winner_id = data.get('winner_id')
    self.loser_id = data.get('loser_id')
    self.created_at = datetime.datetime.utcnow()
    self.modified_at = datetime.datetime.utcnow()

  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    for key, item in data.items():
      setattr(self, key, item)
    self.modified_at = datetime.datetime.utcnow()
    db.session.commit()

  @staticmethod
  def get_all_games():
    return GameModel.query.all()

  @staticmethod
  def get_all_users_games(id, page):
    return GameModel.query.filter(or_(GameModel.organiser_id==id, GameModel.opponent_id==id)).\
                           filter(GameModel.status != 'completed').\
                           order_by(GameModel.game_date.asc()).\
                           order_by(GameModel.game_time.asc()).\
                           paginate(page=int(page), per_page=7, error_out=True).items
  
  @staticmethod
  def get_one_game(id):
    return GameModel.query.get(id)

  @staticmethod
  def get_games_by_id(value):
    return GameModel.query.filter_by(id=value)

  def __repr__(self):
    return '<id {}>'.format(self.id)


class GameSchema(Schema):
  id = fields.Int(dump_only=True)
  organiser_id = fields.Int(required=True)
  opponent_id = fields.Int(required=True)
  game_date = fields.Date(required=True)
  game_time = fields.Time(required=True)
  status = fields.String(required=True)
  sport = fields.String(required=False)
  venue = fields.String(required=False)
  winner_id = fields.Int(required=False)
  loser_id = fields.Int(required=False)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  organiser = fields.Nested('PlayerSchema')
  opponent = fields.Nested('PlayerSchema')
  winner = fields.Nested('PlayerSchema')
  loser = fields.Nested('PlayerSchema')
