from flask import request, json, Response, Blueprint
from ..models.ResultModel import ResultModel, ResultSchema
from ..models.GameModel import GameModel, GameSchema

result_api = Blueprint('result_api', __name__)
result_schema = ResultSchema()

@result_api.route('/', methods=['GET'])
def get_all():
    # results = ResultModel.get_all_results()
    results = GameModel.get_game_by_org_id(1)
    data = result_schema.dump(results, many=True)
    return custom_response(data, 200)

def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
