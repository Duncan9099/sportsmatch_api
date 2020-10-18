from flask import request, json, Response, Blueprint, g, render_template
from ..models.PlayerModel import PlayerModel, PlayerSchema
from ..models.PhotoModel import PhotoModel, PhotoSchema
from .helpers import custom_response
from ..shared.Authentication import Auth

player_api = Blueprint('player', __name__)
player_schema = PlayerSchema()
photo_schema = PhotoSchema()

@player_api.route('/new', methods=['POST'])
def create():
    try:
        req_data = request.get_json()
        data = player_schema.load(req_data)
        player_in_db = PlayerModel.get_player_by_email(data.get('email'))

        if player_in_db:
            message = {'error': 'Email is already in use.  If you have already created an account go to Login.  If not, please use a different email address'}
            return custom_response(message, 400)

        if not data.get("first_name") or not data.get("last_name"): 
            message = {'error': 'Please enter both your first and last name'}
            return custom_response(message, 400)

        if not data.get("email"): 
            message = {'error': 'Please enter you email address'}

        if len(data.get('password')) < 8: 
            message = {'error': 'Password is too short.  Please use at least 8 characters'}
            return custom_response(message, 400)
            
        player = PlayerModel(data)
        player.save()
        player_data = player_schema.dump(player)
        token = Auth.generate_token(player_data.get('id'))
        return custom_response({'jwt_token': token, 'user_id': player_data.get('id')}, 201)
    except:
        pass
        
    
@player_api.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()
    data = player_schema.load(req_data, partial=True)
    player = PlayerModel.get_player_by_email(data.get('email'))

    if not data.get('email') or not data.get('password'):
        return custom_response({'error': 'Please enter both your email and password to continue'}, 400)
    
    if not player:
        return custom_response({'error': 'An account by this email address does not exist.  Please check that you have entered the correct email or create a new account'}, 400)

    if not player.check_hash(data.get('password')):
        return custom_response({'error': 'The password that you have submitted is invalid.  Please try again.'}, 400)

    player.update(data)
    player_data = player_schema.dump(player)
    token = Auth.generate_token(player_data.get('id'))
    return custom_response({
        'jwt_token': token, 
        'user_id': player_data.get('id'),
        'profile_image': player_data.get('profile_image')
    }, 200)


@player_api.route('/fblogin', methods=['POST'])
def fblogin():
    req_data = request.get_json()
    data = player_schema.load(req_data, partial=True)
    player = PlayerModel.get_player_by_email(data.get('email'))

    if not player:
        player = PlayerModel(data)
        player.save()
        player_data = player_schema.dump(player)
        token = Auth.generate_token(player_data.get('id'))
        return custom_response({'jwt_token': token, 'user_id': player_data.get('id')}, 201)

    player.update(data)
    player_data = player_schema.dump(player)
    token = Auth.generate_token(player_data.get('id'))
    return custom_response({
        'jwt_token': token, 
        'user_id': player_data.get('id'),
        'profile_image': player_data.get('profile_image')
    }, 200)

@player_api.route('/my_profile', methods=['GET'])
@Auth.auth_required
def get_current_user():
    user_id = Auth.current_user_id()
    player = PlayerModel.get_one_player(user_id)
    player_data = player_schema.dump(player)

    return custom_response(player_data, 200)


# delete this method if searchplayers screeen migrates away from swiping
@player_api.route('/filter', methods=['POST'])
@Auth.auth_required
def get_all_players():
    user_id = Auth.current_user_id()
    req_data = request.get_json() 
    data = player_schema.load(req_data, partial=True)
    player = PlayerModel.get_filtered_players(
        user_id, data, request.headers.get('page'), request.headers.get('distance')
    )

    if not player:
        message = {'error': 'There are no players in your area'}
        return custom_response(message, 400)

    player_data = player_schema.dump(player, many=True)
    return custom_response(player_data, 200)


@player_api.route('/random', methods=['POST'])
@Auth.auth_required
def get_random_player_with_filters():
    user_id = Auth.current_user_id()
    req_data = request.get_json()
    data = player_schema.load(req_data, partial=True)
    player = PlayerModel.get_filtered_players(
        user_id, data, request.headers.get('page'), request.headers.get('distance')
    )[0]

    if not player:
        message = {'error': 'There are no players in your area'}
        return custom_response(message, 400)

    player_data = player_schema.dump(player)
    return custom_response(player_data, 200)


@player_api.route('/my_profile', methods=['PATCH'])
@Auth.auth_required
def update():
    req_data = request.get_json()
    user_id = Auth.current_user_id()
    player = PlayerModel.get_one_player(user_id)

    if 'sport' in req_data:
        player.update_sport(req_data)
    else:
        data = player_schema.load(req_data, partial=True)
        player.update(data, user_id)

    player_data = player_schema.dump(player)
    return custom_response(player_data, 200)

