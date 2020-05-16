from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.PhotoModel import PhotoModel, PhotoSchema
from .helpers import custom_response

photo_api = Blueprint('photo_api', __name__)
photo_schema = PhotoSchema()

@photo_api.route('/', methods=['POST'])
@Auth.auth_required
def create(): 
    req_data = request.get_json()
    data = photo_schema.load(req_data)
    photos = PhotoModel(data)
    photos.save()
    data = photo_schema.dump(photos)
    return custom_response(data, 200)

@photo_api.route('/', methods=['GET'])
@Auth.auth_required
def get_photos(): 
    photos = PhotoModel.get_photos(Auth.current_user_id())

    if not photos: 
        message = {'error': 'No photos found'}
        return custom_response(message, 400)
        
    data = photo_schema.dump(photos)
    return custom_response(data, 200)

@photo_api.route('/<int:user_id>/', methods=['GET'])
@Auth.auth_required
def get_player_photos(user_id): 
    photos = PhotoModel.get_photos(user_id)
    data = photo_schema.dump(photos)
    return custom_response(data, 200)

@photo_api.route('/', methods=['PATCH'])
@Auth.auth_required
def update(): 
    user_id = Auth.current_user_id()
    req_data = request.get_json()
    data = photo_schema.load(req_data, partial=True)
    photos = PhotoModel.get_photos(Auth.current_user_id())
    photos.update(data, user_id)
    photo_data = photo_schema.dump(photos)
    return custom_response(photo_data, 201)