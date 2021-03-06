from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.GameModel import GameModel, GameSchema
from ..models.PlayerModel import PlayerModel, PlayerSchema
from ..models.ResultModel import ResultModel, ResultSchema
from .helpers import custom_response

game_api = Blueprint('game_api', __name__)
game_schema = GameSchema()
player_schema = PlayerSchema()
result_schema = ResultSchema()


@game_api.route('/<int:game_id>', methods=['GET'])
@Auth.auth_required
def get_one(game_id):
  game = GameModel.get_one_game(game_id)

  if not game:
    return custom_response({'error': 'game not found'}, 404)

  data = game_schema.dump(game)
  return custom_response(data, 200)


@game_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
    user_id = Auth.current_user_id()
    games = GameModel.get_all_users_games(user_id, request.headers.get('page'))

    if not games: 
      message = {'error': 'No Games Scheduled'}
      return custom_response(message, 400)

    data = game_schema.dump(games, many=True)
    return custom_response(data, 200)


@game_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
  req_data = request.get_json()
  data = game_schema.load(req_data)
  game = GameModel(data)
  game.save()
  data = game_schema.dump(game)
  return custom_response(data, 201)


@game_api.route('/<int:game_id>/edit', methods=['PATCH'])
@Auth.auth_required
def edit_game(game_id):
    user_id = Auth.current_user_id()
    req_data = request.get_json()
    game = GameModel.get_one_game(game_id)
    data = game_schema.dump(game)
    if not game:
        return custom_response({'error': 'game not found'}, 404)
    if data.get('organiser_id') == user_id\
        or data.get('opponent_id') == user_id:
            data = game_schema.load(req_data, partial=True)
            game.update(data)
            data = game_schema.dump(game)
            return custom_response(data, 201)


@game_api.route('/results', methods=['GET'])
@Auth.auth_required
def get_all_results():
    user_id = Auth.current_user_id()
    results = GameModel.get_all_users_results(user_id, request.headers.get('page'))
    if not results:
        message = {"error": "No Results Found"}
        return custom_response(message, 400)

    data = game_schema.dump(results, many=True)
    return custom_response(data, 200)


@game_api.route('/statistics', methods=['GET'])
@Auth.auth_required
def get_player_statistics():
    user_id = Auth.current_user_id()
    statistics = GameModel.get_player_statistics(user_id)
    return custom_response(statistics, 200)


@game_api.route('/statistics/<string:sport>', methods=['GET'])
@Auth.auth_required
def get_player_statistics_by_sport(sport):
    user_id = Auth.current_user_id()
    statistics = GameModel.get_player_statistics_by_sport(user_id, sport)
    return custom_response(statistics, 200)
