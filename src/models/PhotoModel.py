from marshmallow import fields, Schema
from . import db
import datetime
import zlib 
import boto3
import botocore
import os
import errno
from botocore.exceptions import ClientError

s3 = boto3.resource('s3')
photo_bucket = s3.Bucket('s3-sportsmatch-user-images')


class PhotoModel(db.Model): 
    __tablename__ = 'photos'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('players.id'), unique=True, nullable=False)
    photo1 = db.Column(db.String(128), nullable=True)
    photo2 = db.Column(db.String(128), nullable=True)
    photo3 = db.Column(db.String(128), nullable=True)
    photo4 = db.Column(db.String(128), nullable=True)
    photo5 = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    user = db.relationship("PlayerModel", primaryjoin = "PhotoModel.user_id == PlayerModel.id", backref="user")

    def __init__(self, data): 
        self.user_id = data.get('user_id')
        self.photo1 = f"{data.get('user_id')}-{data.get('photo1')}"
        self.photo2 = f"{data.get('user_id')}-{data.get('photo2')}"
        self.photo3 = f"{data.get('user_id')}-{data.get('photo3')}" 
        self.photo4 = f"{data.get('user_id')}-{data.get('photo4')}" 
        self.photo5 = f"{data.get('user_id')}-{data.get('photo5')}"
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data, user_id):
        for key, item in data.items():
            filename = self.writeFile(key, item, user_id)
            filepath = f'http://s3.aws.amazon.com/s3-sportsmatch-user-images/{user_id}-{key}'
            # photo_bucket.put_object(Key=filepath, Body=)
            self.uploadFile(filename, user_id, key)
            setattr(self, key, filepath)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def uploadFile(self, file_name, user_id, key):
        try:
            key = f'{user_id}/{key}'
            response = photo_bucket.upload_file(file_name, key, ExtraArgs={'ACL':'public-read'})
        except ClientError as e:
            print(e)
            return False
        return True


    def writeFile(self, key, item, user_id): 
        filename = f'./src/storage/{user_id}/{key}.txt'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            f.write(f'{item}')
        
        return filename

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
    photo1 = fields.Str(required=False)
    photo2 = fields.Str(required=False)
    photo3 = fields.Str(required=False)
    photo4 = fields.Str(required=False)
    photo5 = fields.Str(required=False)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)