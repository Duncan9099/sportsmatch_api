from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.FriendModel import FriendModel, FriendSchema
from .helpers import custom_response

friend_api = Blueprint('friend_api', __name__)
friend_schema = FriendSchema()

@friend_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    req_data = request.get_json()
    data = friend_schema.load(req_data)
    friendship_exists = FriendModel.does_friendship_exist(req_data['requester_id'], req_data['responder_id'])
    if friendship_exists.count() > 0:
        message = {"error": "You are already friends"}
        return custom_response(message, 400)
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

    if requests.count() < 1:
        message = {"error": "No Requests Found"}
        return custom_response(message, 400)

    data = friend_schema.dump(requests, many=True)
    return custom_response(data, 201)

@friend_api.route('/all', methods=['GET'])
@Auth.auth_required
def get_friends(): 
    user_id = Auth.current_user_id() 
    friends = FriendModel.get_all_friends(user_id)

    if friends.count() < 1:
        message = {"error": "No Friends Found"}
        return custom_response(message, 400)

    data = friend_schema.dump(friends, many=True) 
    return custom_response(data, 200)

@friend_api.route('/<int:friend_request_id>', methods=['DELETE'])
@Auth.auth_required
def delete(friend_request_id): 
    request = FriendModel.get_friend_request(friend_request_id)
    request.delete()
    return custom_response({'message': 'request deleted'}, 200)

@friend_api.route('/<int:friend_request_id>', methods=['GET'])
@Auth.auth_required
def get_friendship_status(friend_request_id):
    user_id = Auth.current_user_id()
    status = FriendModel.does_friendship_exist(user_id, friend_request_id)
    if status.count() > 0:
        message = {"friends": True}
        return custom_response(message, 200)

    if status.count() <= 0:
        message = {"friends": False}
        return custom_response(message, 200)