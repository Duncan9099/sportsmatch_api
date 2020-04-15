from marshmallow import fields, Schema
from . import db
import datetime

class PhotoModel(db.Model): 
    __tablename__ = 'photos'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('players.id'), unique=True, nullable=False)
    photo1 = db.Column(db.LargeBinary, nullable=True)
    photo2 = db.Column(db.LargeBinary, nullable=True)
    photo3 = db.Column(db.LargeBinary, nullable=True)
    photo4 = db.Column(db.LargeBinary, nullable=True)
    photo5 = db.Column(db.LargeBinary, nullable=True)
    photo6 = db.Column(db.LargeBinary, nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    user = db.relationship("PlayerModel", primaryjoin = "PhotoModel.user_id == PlayerModel.id", backref="user")

    def __init__(self, data): 
        self.user_id = data.get('user_id')
        self.photo1 = data.get('photo1')
        self.photo2 = data.get('photo2')
        self.photo3 = data.get('photo3') 
        self.photo4 = data.get('photo4') 
        self.photo5 = data.get('photo5')
        self.photo6 = data.get('photo6')
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

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @staticmethod 
    def get_photos(id):
        return PhotoModel.query.filter(PhotoModel.user_id==id).first()
        
class BytesField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return ""
        binary_string = bin(int.from_bytes(value.encode(), 'big'))
        binary = bytes(binary_string, 'utf-8')
        return binary

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        binary_string = int(value,2)
        base64_string = binary_string.to_bytes((binary_string.bit_length() + 7) // 8, 'big').decode()
        return base64_string
    
class PhotoSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    photo1 = BytesField(required=False)
    photo2 = BytesField(required=False)
    photo3 = BytesField(required=False)
    photo4 = BytesField(required=False)
    photo5 = BytesField(required=False)
    photo6 = BytesField(required=False)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)