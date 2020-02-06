from flask import g, request, json, Response, Blueprint
from ..models.PlayerModel import PlayerModel
from ..models.ResultModel import ResultModel, ResultSchema
from ..models.GameModel import GameModel, GameSchema
from ..shared.Authentication import Auth

result_api = Blueprint('results', __name__)
result_schema = ResultSchema()
game_schema = GameSchema()

@result_api.route('/<int:game_id>/new', methods=['POST'])
@Auth.auth_required
def create(game_id):
        current_user_id = Auth.current_user_id()
        req_data = request.get_json()
        winner = PlayerModel.get_one_player(req_data['winner_id'])
        loser = PlayerModel.get_one_player(req_data['loser_id'])
        data = result_schema.load(req_data)
        result = ResultModel.get_result_by_game(game_id)
        if result:
          message = {'error': 'Result already provided'}
          return custom_response(message, 400)
        game = GameModel.get_one_game(game_id)
    #   if game.status != "confirmed":
    #       message = {'error': 'Game needs to be confirmed to add a result'}
    #       return custom_response(message, 400)
    #   if game.organiser_id == current_user_id:
        result = ResultModel(data)
        # winner.update_winner_rank_points()
        # loser.update_loser_rank_points()
        result.save()
        return custom_response(data, 201)
    #   message = {'error': 'You can only add a result if you are the organiser.'}
    #   return custom_response(message, 400)

@result_api.route('/', methods=['GET'])
@Auth.auth_required
def get_player_results(): 
    user_id = Auth.current_user_id()
    results = ResultModel.get_player_results(user_id)
    data = result_schema.dump(results, many=True)
    return custom_response(data, 200)

def custom_response(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
