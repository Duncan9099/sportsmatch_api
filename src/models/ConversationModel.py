import datetime
from . import db
from marshmallow import fields, Schema
from sqlalchemy import or_
from .PlayerModel import PlayerModel, PlayerSchema


class ConversationModel(db.Model):
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True)
    send_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    receive_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    send_read = db.Column(db.Boolean, default=False, nullable=False)
    receive_read = db.Column(db.Boolean, default=False, nullable=False)
    send = db.relationship("PlayerModel", primaryjoin="ConversationModel.send_id == PlayerModel.id", backref="send")
    receive = db.relationship("PlayerModel", primaryjoin="ConversationModel.receive_id == PlayerModel.id", backref="receive")

    def __init__(self, data):
        self.send_id = data.get('send_id')
        self.receive_id = data.get('receive_id')
        self.send_read = data.get('send_read')
        self.receive_read = data.get('receive_read')
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
    def get_conversations(user_id):
        return ConversationModel.query.filter(or_(ConversationModel.send_id==user_id, ConversationModel.receive_id==user_id))

    @staticmethod
    def conversation_exists(user_id, other_user_id):
        result = ConversationModel.query.filter(ConversationModel.get_conversations(user_id)).\
                                        filter(or_(ConversationModel.send_id==other_user_id, ConversationModel.receive_id==other_user_id))
        if result.count() < 1:
            return False
        return True

    def __repr__(self):
        return '<id {}>'.format(self.id)


class ConversationSchema(Schema):
    id = fields.Int(dump_only=True)
    send_id = fields.Int(required=True)
    receive_id = fields.Int(required=True)
    send_read = fields.Boolean(required=False)
    receive_read = fields.Boolean(required=False)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    send = fields.Nested('PlayerSchema')
    receive = fields.Nested('PlayerSchema')
