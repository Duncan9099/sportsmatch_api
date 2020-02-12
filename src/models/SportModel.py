import datetime
from . import db # import db instance from models/__init__.py
from marshmallow import fields, Schema
from sqlalchemy import or_

class SportModel(db.Model): 
    __tablename__ = 'sports'

    id = db.Column(db.Integer, primary_key=True)
    current_user_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False, unique=True)
    tennis = db.Column(db.String(50), default="None", nullable=True)
    squash = db.Column(db.String(50), default="None", nullable=True)
    table_tennis = db.Column(db.String(50), default="None", nullable=True)
    badminton = db.Column(db.String(50), default="None", nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    current_user = db.relationship("PlayerModel", primaryjoin = "SportModel.current_user_id == PlayerModel.id", backref="current_user")

    def __init__(self, data): # class constructor used to set the class attributes
        self.current_user_id = data.get('current_user_id')
        self.tennis = data.get('tennis')
        self.squash = data.get('squash')
        self.table_tennis = data.get('table_tennis')
        self.badminton = data.get('badminton')
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

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_sports(id): 
        return SportModel.query.filter(SportModel.current_user_id==id)
    
    @staticmethod
    def filter_sports(data):
        return SportModel.query.filter(or_(SportModel.tennis==data.get('tennis'), 
                                        SportModel.badminton==data.get('badminton'), 
                                        SportModel.squash==data.get('squash'), 
                                        SportModel.table_tennis==data.get('table_tennis')))

    def __repr__(self):
        return '<id {}>'.format(self.id)

class SportSchema(Schema): 
    id = fields.Int(dump_only=True)
    current_user_id = fields.Int(required=True) 
    tennis = fields.Str(required=False)
    squash = fields.Str(required=False)
    table_tennis = fields.Str(required=False)
    badminton = fields.Str(required=False)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    current_user = fields.Nested('PlayerSchema')
