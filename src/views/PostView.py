from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.PostModel import PostModel, PostSchema
# from ..models.PlayerModel import PlayerModel

post_api = Blueprint('post_api', __name__)
post_schema = PostSchema()

def custom_response(res, status_code):
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )

@post_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    req_data = request.get_json()
    data = post_schema.load(req_data)
    post = PostModel(data)
    post.save()
    data = post_schema.dump(post)
    return custom_response(data, 200)

@post_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all_posts():
    post = PostModel.get_all_posts().first()
    if not post:
        return custom_response({'message': 'no previous posts'}, 400)
    posts = PostModel.get_all_posts()
    data = post_schema.dump(posts, many=True)
    return custom_response(data, 200)
