from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.FriendModel import FriendModel, FriendSchema

friend_api = Blueprint('friend_api', __name__)
friend_schema = FriendSchema()

def custom_response(res, status_code): 
    return Response(
        mimetype="application/json", 
        response=json.dumps(res), 
        status=status_code
    )

@friend_api.route('/', methods=['POST'])
@Auth.auth_required
def create(): 
    req_data = request.get_json() 
    data = friend_schema.load(req_data)
    friend = FriendModel(data)
    friend.save()
    data = friend_schema.dump(friend)
    return custom_response(data, 201)

@friend_api.route('/<int:friend_request_id>', methods=['PATCH'])
@Auth.auth_required
def update(friend_request_id): 
    user_id = Auth.current_user_id() 
    req_data = request.get_json()
    friend = FriendModel.get_friend_request(friend_request_id)
    data = friend_schema.dump(friend)
    if not friend: 
        return custom_response({'error': 'friend request not found'}, 400)
    if data.get('responder_id') != user_id:
        return custom_response({'error': 'response not permitted'}, 400)
    if data.get('responder_id') == user_id: 
        data = friend_schema.load(req_data, partial=True) 
        friend.update(data)
        data = friend_schema.dump(friend) 
        return custom_response(data, 201)

@friend_api.route('/', methods=['GET'])
@Auth.auth_required
def get_requests(): 
    user_id = Auth.current_user_id() 
    requests = FriendModel.get_all_friend_requests(user_id)
    data = friend_schema.dump(requests, many=True)
    return custom_response(data, 201)