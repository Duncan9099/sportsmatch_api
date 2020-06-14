import datetime
from . import db # import db instance from models/__init__.py
from marshmallow import fields, Schema
from sqlalchemy import or_


class ResultModel(db.Model): # ResultModel class inherits from db.Model
    __tablename__ = 'results' # name our table Results

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False, unique=True)
    winner_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    loser_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    result_confirmed = db.Column(db.Boolean, default=False, nullable=False)
    sport = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    winner = db.relationship("PlayerModel", primaryjoin="ResultModel.winner_id == PlayerModel.id", backref="winner")
    loser = db.relationship("PlayerModel", primaryjoin="ResultModel.loser_id == PlayerModel.id", backref="loser")
    game = db.relationship("GameModel", back_populates="result")

    def __init__(self, data): # class constructor used to set the class attributes
        self.game_id = data.get('game_id')
        self.winner_id = data.get('winner_id')
        self.loser_id = data.get('loser_id')
        self.sport = data.get('sport')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def count_total_games_played(id):
        result = ResultModel.query.filter(or_(ResultModel.winner_id == id, ResultModel.loser_id == id))
        return result.count()

    @staticmethod
    def count_total_wins(id):
        result = ResultModel.query.filter(ResultModel.winner_id == id)
        return result.count()

    @staticmethod
    def count_games_by_sport(id, sport):
        result = ResultModel.query.filter(or_(ResultModel.winner_id == id, ResultModel.loser_id == id)).\
                                          filter(sport == sport)
        return result.count()

    @staticmethod
    def count_wins_by_sport(id, sport):
        result = ResultModel.query.filter(ResultModel.winner_id == id, sport == sport)
        return result.count()

    @staticmethod
    def count_loses_by_sport(id, sport):
        games = ResultModel.count_games_by_sport(id, sport)
        wins = ResultModel.count_wins_by_sport(id, sport)
        loses = games - wins
        return loses

    @staticmethod
    def get_player_statistics_by_sport(id, sport):
        statistics = {}
        statistics['games'] = ResultModel.count_games_by_sport(id, sport)
        statistics['wins'] = ResultModel.count_wins_by_sport(id, sport)
        statistics['loses'] = ResultModel.count_loses_by_sport(id, sport)
        return statistics

    @staticmethod
    def count_total_loses(id):
        total_games = ResultModel.count_total_games_played(id)
        wins = ResultModel.count_total_wins(id)
        loses = total_games - wins
        return loses

    @staticmethod
    def get_result_by_game(value):
        return ResultModel.query.filter_by(game_id=value).first()

    @staticmethod
    def get_all_results(value):
        return ResultModel.query.filter_by(game_id=value)

    @staticmethod
    def get_player_results(id, page): 
        return ResultModel.query.filter(or_(ResultModel.winner_id==id, ResultModel.loser_id==id)).\
            paginate(page=int(page), per_page=7, error_out=True).items

    @staticmethod
    def get_player_statistics(id):
        statistics = {}
        statistics['total_games'] = ResultModel.count_total_games_played(id)
        statistics['total_wins'] = ResultModel.count_total_wins(id)
        statistics['total_loses'] = ResultModel.count_total_loses(id)
        return statistics

    def __repr__(self):
        return '<id {}>'.format(self.id)

class ResultSchema(Schema):
    id = fields.Int(dump_only=True)
    game_id = fields.Int(required=True)
    winner_id = fields.Int(required=False)
    loser_id = fields.Int(required=False)
    sport = fields.String(required=False)
    result_confirmed = fields.Boolean(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    winner = fields.Nested('PlayerSchema')
    loser = fields.Nested('PlayerSchema') 
    game = fields.Nested('GameSchema')