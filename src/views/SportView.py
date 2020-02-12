from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.SportModel import SportModel, SportSchema

sport_api = Blueprint('sport_api', __name__)
sport_schema = SportSchema()

def custom_response(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )

@sport_api.route('/', methods=['POST'])
@Auth.auth_required
def create(): 
    req_data = request.get_json()
    data = sport_schema.load(req_data)
    sports = SportModel(data)
    sports.save()
    data = sport_schema.dump(sports)
    return custom_response(data, 200)

@sport_api.route('/', methods=['PATCH'])
@Auth.auth_required
def update(): 
    user_id = Auth.current_user_id()
    req_data = request.get_json() 
    sports = SportModel.get_sports(user_id)
    data = sport_schema.dump(sports)
    data = sport_schema.load(req_data, partial=True)
    sports.update(data)
    data = sport_schema.dump(sports, many=True)
    return custom_response(data, 200)

@sport_api.route('/filter', methods=['POST'])
@Auth.auth_required
def get_filtered_sports(): 
    user_id = Auth.current_user_id()
    req_data = request.get_json()
    data = sport_schema.load(req_data, partial=True)
    filtered_players = SportModel.filter_sports(data)
    player_data = sport_schema.dump(filtered_players, many=True)
    return custom_response(player_data, 200)

