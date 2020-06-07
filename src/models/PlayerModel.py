from marshmallow import fields, Schema
from sqlalchemy.orm import load_only
import datetime
from . import db # import db instance from models/__init__.py
from ..app import bcrypt
from .GameModel import GameSchema
from .ResultModel import ResultSchema
from sqlalchemy import or_
import pgeocode
import requests
import boto3
import botocore
import os
import errno
from botocore.exceptions import ClientError

s3 = boto3.resource('s3')
photo_bucket = s3.Bucket('s3-sportsmatch-user-images')


class PlayerModel(db.Model):
  __tablename__ = 'players'

  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(60), nullable=False)
  last_name = db.Column(db.String(60), nullable=True)
  email = db.Column(db.String(128), unique=True, nullable=False)
  password = db.Column(db.String(128), nullable=False)
  postcode = db.Column(db.String(20), nullable=True)
  gender = db.Column(db.String(50), nullable=True)
  dob = db.Column(db.Date, nullable=True)
  profile_image = db.Column(db.String(128), nullable=True)
  bio = db.Column(db.String(200), nullable=True)
  tennis = db.Column(db.String(50), default="None", nullable=True)
  squash = db.Column(db.String(50), default="None", nullable=True)
  table_tennis = db.Column(db.String(50), default="None", nullable=True)
  badminton = db.Column(db.String(50), default="None", nullable=True)
  latitude = db.Column(db.Float, nullable=True)
  longitude = db.Column(db.Float, nullable=True)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)

  # class constructor to set class attributes
  def __init__(self, data):
    self.first_name = data.get('first_name')
    self.last_name = data.get('last_name')
    self.email = data.get('email')
    self.password = self.__generate_hash(data.get('password'))
    self.gender = data.get('gender')
    self.dob = data.get('dob')
    self.bio = data.get('bio')
    self.tennis = data.get('tennis')
    self.squash = data.get('squash')
    self.table_tennis = data.get('table_tennis')
    self.badminton = data.get('badminton')
    self.created_at = datetime.datetime.utcnow()
    self.modified_at = datetime.datetime.utcnow()
    self.profile_image = data.get('profile_image')
    self.postcode = data.get('postcode')
    self.latitude = data.get('latitude') 
    self.longitude = data.get('longitude')

  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data, user_id=None):
    for key, item in data.items():
        if key == 'password':
            setattr(self, 'password', self.__generate_hash(item))
        elif key == 'profile_image': 
            filename = self.writeFile(key, item, user_id)
            filepath = f'http://s3.aws.amazon.com/s3-sportsmatch-user-images/{user_id}/{key}'
            self.uploadFile(filename, user_id, key)
            setattr(self, key, filepath)
        else:
            setattr(self, key, item)
    self.modified_at = datetime.datetime.utcnow()
    db.session.commit()

  def __generate_hash(self, password):
    return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

  def check_hash(self, password):
    return bcrypt.check_password_hash(self.password, password)
  
  def uploadFile(self, file_name, user_id, key):
        try:
            key = f'{user_id}/profile_image'
            response = photo_bucket.upload_file(file_name, key, ExtraArgs={'ACL':'public-read'})
        except ClientError as e:
            print(e)
            return False
        return True

  def writeFile(self, key, item, user_id): 
        filename = f'./src/storage/{user_id}/profile.txt'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            f.write(f'{item}')
        
        return filename

  @staticmethod
  def get_player_by_email(value):
    return PlayerModel.query.filter_by(email=value).first()

  @staticmethod
  def get_player_profile_image(id):
    return PlayerModel.query.with_entities(PlayerModel.profile_image).filter_by(id=id).first()

  @staticmethod
  def get_one_player(id):
    return PlayerModel.query.get(id)

  @staticmethod
  def get_opponent_info(id):
    player_schema = PlayerSchema()
    player = PlayerModel.query.with_entities(PlayerModel.first_name).filter_by(id=id).first()
    return player_schema.dump(player)

  @staticmethod
  def get_filtered_players(id, data, page, distance):
    user_schema = PlayerSchema()
    user = PlayerModel.query.filter_by(id=id).first()
    serialized_user = user_schema.dump(user)
    players = PlayerModel.get_players_by_ability(data, page)
    return PlayerModel.get_players_within_distance(players, serialized_user, distance)

  @staticmethod
  def get_player_location(postcode):
    req_data = requests.get(f'https://api.postcodes.io/postcodes/{postcode}').json()
    if req_data['status'] == 200:
      return(req_data['result']['admin_district'])
    return(req_data['error'])

  @staticmethod
  def get_players_by_ability(data, page):
    return PlayerModel.query.filter(or_(
                PlayerModel.tennis==data.get('tennis'), 
                PlayerModel.badminton==data.get('badminton'), 
                PlayerModel.squash==data.get('squash'), 
                PlayerModel.table_tennis==data.get('table_tennis'))).\
                paginate(page=int(page), per_page=4, error_out=True).items

  @staticmethod
  def get_players_within_distance(players, user, distance):
      user_location = [user['latitude'], user['longitude']]
      filtered_array = []
      for player in players:
          player_location = [player.latitude, player.longitude]
          distances_between_players = int(PlayerModel.get_distance_between_postcodes([user_location], [player_location]))
          if distances_between_players <= int(distance):
              filtered_array.append(player)
      return filtered_array

  @staticmethod
  def get_distance_between_postcodes(org_code, opp_code):
    return pgeocode.haversine_distance(org_code, opp_code)

  @staticmethod
  def get_player_postcode(id):
      player_schema = PlayerSchema()
      player = PlayerModel.query.with_entities(PlayerModel.postcode).filter_by(id=id).first()
      return player_schema.dump(player)

  def __repr__(self): # returns a printable representation of the PlayerModel object (returning the id only)
    return '<id {}>'.format(self.id)

class Postcode(fields.Field):
    """
    Creating custom field for scheme that serializes base64 to LargeBinary
    and deserializes LargeBinary to base64
    """
    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return ""
        return value.upper().replace(' ', '')

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        return value

class BytesField(fields.Field):
    """
    Creating custom field for schema that deserializes base64 to LargeBinary
    and serializes LargeBinary to base64
    """
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

class PlayerSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=False)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    gender = fields.Str(required=False)
    dob = fields.Date(required=False)
    profile_image = fields.Str(required=False)
    bio = fields.Str(required=False)
    tennis = fields.Str(required=False)
    squash = fields.Str(required=False)
    table_tennis = fields.Str(required=False)
    badminton = fields.Str(required=False)
    latitude = fields.Float(required=False) 
    longitude = fields.Float(required=False)
    postcode = Postcode(required=False)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)