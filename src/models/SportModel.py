import datetime
from . import db # import db instance from models/__init__.py
from marshmallow import fields, Schema
from sqlalchemy import or_

class SportModel(db.Model): 
    __tablename__ = 'sports'

    id = db.Column(db.Integer, primary_key=True)
    current_user_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False, unique=True)
    tennis = db.Column(db.Boolean, default=False, nullable=True)
    tennis_ability = db.Column(db.String(20), default='Beginner', nullable=True)
    squash = db.Column(db.Boolean, default=False, nullable=True)
    squash_ability = db.Column(db.String(20), default='Beginner', nullable=True)
    table_tennis = db.Column(db.Boolean, default=False, nullable=True)
    table_tennis_ability = db.Column(db.String(20), default='Beginner', nullable=True)
    badminton = db.Column(db.Boolean, default=False, nullable=True)
    badminton_ability = db.Column(db.String(20), default='Beginner', nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    current_user = db.relationship("PlayerModel", primaryjoin = "SportModel.current_user_id == PlayerModel.id", backref="current_user")

    def __init__(self, data): # class constructor used to set the class attributes
        self.current_user_id = data.get('current_user_id')
        self.tennis = data.get('tennis')
        self.tennis_ability = data.get('tennis_ability')
        self.squash = data.get('squash')
        self.squash_ability = data.get('squash_ability')
        self.table_tennis = data.get('table_tennis')
        self.table_tennis_ability = data.get('table_tennis_ability')
        self.badminton = data.get('badminton')
        self.badminton_ability = data.get('badminton_ability')
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

    def __repr__(self):
        return '<id {}>'.format(self.id)

class SportSchema(Schema): 
    id = fields.Int(dump_only=True)
    current_user_id = fields.Int(required=True) 
    tennis = fields.Boolean(required=False)
    tennis_ability = fields.Str(required=False)
    squash = fields.Boolean(required=False)
    squash_ability = fields.Str(required=False)
    table_tennis = fields.Boolean(required=False)
    table_tennis_ability = fields.Str(required=False)
    badminton = fields.Boolean(required=False)
    badminton_ability = fields.Str(required=False)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    current_user = fields.Nested('PlayerSchema')
