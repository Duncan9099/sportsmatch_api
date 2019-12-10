import datetime
from . import db # import db instance from models/__init__.py
from marshmallow import fields, Schema
from sqlalchemy.orm import load_only
import requests
from .PlayerModel import BytesField

class PostModel(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    image = db.Column(db.LargeBinary, nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    user = db.relationship('PlayerModel', primaryjoin="PostModel.user_id == PlayerModel.id", backref='user')

    def __init__(self, data):
        self.user_id = data.get('user_id')
        self.content = data.get('content')
        self.image = data.get('image')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<id {}>'.format(self.id)

# class BytesField(fields.Field):
#     """
#     Creating custom field for schema that deserializes base64 to LargeBinary
#     and serializes LargeBinary to base64
#     """
#     def _deserialize(self, value, attr, data, **kwargs):
#         if value is None:
#             return ""
#         binary_string = bin(int.from_bytes(value.encode(), 'big'))
#         binary = bytes(binary_string, 'utf-8')
#         return binary
#
#     def _serialize(self, value, attr, obj, **kwargs):
#         if value is None:
#             return ""
#         binary_string = int(value,2)
#         base64_string = binary_string.to_bytes((binary_string.bit_length() + 7) // 8, 'big').decode()
#         return base64_string

class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    content = fields.Str(required=True)
    image = BytesField(required=False)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
