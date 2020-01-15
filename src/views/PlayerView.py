from flask import request, json, Response, Blueprint, g, render_template
from ..models.PlayerModel import PlayerModel, PlayerSchema
from ..shared.Authentication import Auth

player_api = Blueprint('player', __name__)
player_schema = PlayerSchema()

@player_api.route('/new', methods=['POST'])
def create():
    req_data = request.get_json()
    data = player_schema.load(req_data)
    player_in_db = PlayerModel.get_player_by_email(data.get('email'))
    if player_in_db:
        message = {'error': 'Player already exist, please supply another email address'}
        return custom_response(message, 400)
    player = PlayerModel(data)
    player.save()
    player_data = player_schema.dump(player)
    token = Auth.generate_token(player_data.get('id'))
    return custom_response({'jwt_token': token, 'user_id': player_data.get('id')}, 201)

@player_api.route('/<int:player_id>/image', methods=['GET'])
@Auth.auth_required
def get_image(player_id):
  player = PlayerModel.get_player_profile_image(player_id)
  player_data = player_schema.dump(player)
  return custom_response(player_data, 200)

@player_api.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()
    data = player_schema.load(req_data, partial=True)
    if not data.get('email') or not data.get('password'):
        return custom_response({'error': 'you need email and password to sign in'}, 400)
    player = PlayerModel.get_player_by_email(data.get('email'))
    if not player:
        return custom_response({'error': 'invalid credentials'}, 400)
    if not player.check_hash(data.get('password')):
        return custom_response({'error': 'invalid password'}, 400)
    player_data = player_schema.dump(player)
    token = Auth.generate_token(player_data.get('id'))
    return custom_response({
        'jwt_token': token, 
        'user_id': player_data.get('id'),
        'profile_image': player_data.get('profile_image'), 
        'first_name': player_data.get('first_name'), 
        'sport': player_data.get('sport'), 
        'ability': player_data.get('ability')
    }, 200)

@player_api.route('/<int:player_id>', methods=['GET'])
@Auth.auth_required
def get_a_player(player_id):
    player = PlayerModel.get_player_info(player_id)
    player_data = player_schema.dump(player)
    player_data_location = {'location': PlayerModel.get_player_location(player_data['postcode'])}
    player_data_combined = {**player_data, **player_data_location}
    if not player:
        return custom_response({'error': 'player not found'}, 404)
    return custom_response(player_data_combined, 200)

@player_api.route('/my_profile', methods=['GET'])
@Auth.auth_required
def get_current_user():
    user_id = Auth.current_user_id()
    player = PlayerModel.get_one_player(user_id)
    player_data = player_schema.dump(player)

    return custom_response(player_data, 200)

@player_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all_players():
    user_id = Auth.current_user_id()
    players = PlayerModel.get_filtered_players(user_id, request.headers.get('ability'), request.headers.get('distance'), request.headers.get('page'))
    players_data = player_schema.dump(players, many=True)
    return custom_response(players_data, 200)

@player_api.route('/my_profile', methods=['PATCH'])
@Auth.auth_required
def update():
    req_data = request.get_json()
    data = player_schema.load(req_data, partial=True)
    user_id = Auth.current_user_id()
    player = PlayerModel.get_one_player(user_id)
    player.update(data)
    player_data = player_schema.dump(player)
    return custom_response(player_data, 200)

# @player_api.route('/my_profile', methods=['DELETE'])
# @Auth.auth_required
# def delete():
#     """
#     Delete logged-in player's account
#     """
#     user_id = Auth.current_user_id()
#     player = PlayerModel.get_one_player(user_id)
#     player.delete()
#
#     return custom_response({'message': 'user deleted'}, 204)

def custom_response(res, status_code):
    return Response(
      mimetype="application/json",
      response=json.dumps(res),
      status=status_code
    )
