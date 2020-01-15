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




