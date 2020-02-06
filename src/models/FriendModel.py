import datetime
from . import db # import db instance from models/__init__.py
from marshmallow import fields, Schema
from sqlalchemy import or_

class FriendModel(db.Model): 
    __tablename__ = 'friends'

    id = db.Column(db.Integer, primary_key=True) 
    requester_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    responder_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    confirmed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime) 
    requester = db.relationship("PlayerModel", primaryjoin="FriendModel.requester_id == PlayerModel.id", backref="requester")
    responder = db.relationship("PlayerModel", primaryjoin="FriendModel.responder_id == PlayerModel.id", backref="responder")

    def __init__(self, data): 
        self.requester_id = data.get('requester_id')
        self.responder_id = data.get('responder_id')
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
    def get_friend_request(request_id): 
        return FriendModel.query.filter(FriendModel.id==request_id).first()

    @staticmethod
    def get_all_friend_requests(responder_id): 
        return FriendModel.query.filter(FriendModel.responder_id==responder_id).\
                                filter(FriendModel.confirmed==False)

    @staticmethod
    def get_all_friends(user_id): 
        return FriendModel.query.filter(_or(FriendModel.responder_id==user_id, FriendModel.request_id==user_id).\
                                filter(FriendModel.confirmed==True))

    def __repr__(self): 
        return '<id {}>'.format(self.id)

class FriendSchema(Schema): 
    id = fields.Int(dump_only=True) 
    requester_id = fields.Int(required=True) 
    responder_id = fields.Int(required=True) 
    confirmed = fields.Boolean(required=False) 
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True) 
    requester = fields.Nested('PlayerSchema') 
    responder = fields.Nested('PlayerSchema')
