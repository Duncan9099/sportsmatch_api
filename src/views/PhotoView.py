from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.PhotoModel import PhotoModel, PhotoSchema

photo_api = Blueprint('photo_api', __name__)
photo_schema = PhotoSchema()

def custom_response(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )

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
    req_data = request.get_json()
    data = photo_schema.load(req_data, partial=True)
    photos = PhotoModel.get_photos(Auth.current_user_id())
    photos.update(data)
    photo_data = photo_schema.dump(photos)
    return custom_response(photo_data, 201)





    




