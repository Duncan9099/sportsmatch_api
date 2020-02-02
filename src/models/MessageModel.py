import datetime
from . import db # import db instance from models/__init__.py
from marshmallow import fields, Schema
from sqlalchemy import or_
from .PlayerModel import PlayerModel, PlayerSchema

class MessageModel(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    sender_read = db.Column(db.Boolean, default=False, nullable=False)
    receiver_read = db.Column(db.Boolean, default=False, nullable=False)
    sender = db.relationship("PlayerModel", primaryjoin = "MessageModel.sender_id == PlayerModel.id", backref="sender")
    receiver = db.relationship("PlayerModel", primaryjoin = "MessageModel.receiver_id == PlayerModel.id", backref="receiver")

    def __init__(self, data):
        self.sender_id = data.get('sender_id')
        self.receiver_id = data.get('receiver_id')
        self.content = data.get('content')
        self.sender_read = data.get('sender_read')
        self.receiver_read = data.get('receiver_read')
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
    def get_all_messages_with_user(current_user_id, other_user_id):
      return MessageModel.query.filter(or_(MessageModel.sender_id==current_user_id, MessageModel.receiver_id==current_user_id)).\
                                filter(or_(MessageModel.sender_id==other_user_id, MessageModel.receiver_id==other_user_id))

    @staticmethod
    def get_users_messages(current_user_id):
      return MessageModel.query.filter(or_(MessageModel.sender_id==current_user_id, MessageModel.receiver_id==current_user_id)).\
                                distinct(MessageModel.sender_id, MessageModel.receiver_id).\
                                paginate(per_page=10, error_out=True).items
    
    @staticmethod
    def get_single_message(message_id): 
      return MessageModel.query.filter(MessageModel.id==message_id).first()

    def __repr__(self):
      return '<id {}>'.format(self.id)

class MessageSchema(Schema):
  id = fields.Int(dump_only=True)
  sender_id = fields.Int(required=True)
  receiver_id = fields.Int(required=True)
  content = fields.Str(required=True)
  sender_read = fields.Boolean(required=False)
  receiver_read = fields.Boolean(required=False)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  sender = fields.Nested('PlayerSchema')
  receiver = fields.Nested('PlayerSchema')