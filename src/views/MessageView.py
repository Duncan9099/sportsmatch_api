from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.MessageModel import MessageModel, MessageSchema
from ..models.PlayerModel import PlayerModel
from .helpers import custom_response

message_api = Blueprint('message_api', __name__)
message_schema = MessageSchema()

@message_api.route('/<int:other_user_id>', methods=['GET'])
@Auth.auth_required
def get_all_messages(other_user_id):
    message = MessageModel.get_all_messages_with_user(Auth.current_user_id(), other_user_id).first()
    if not message:
        return custom_response({'error': 'No previous messages, start your conversation now'}, 200)
    messages = MessageModel.get_all_messages_with_user(Auth.current_user_id(), other_user_id)
    data = message_schema.dump(messages, many=True)
    player = PlayerModel.get_player_postcode(Auth.current_user_id())
    return custom_response(data, 200)

@message_api.route('/<int:message_id>', methods=['PATCH'])
@Auth.auth_required
def update(message_id): 
    req_data = request.get_json()
    data = message_schema.load(req_data, partial=True)
    message = MessageModel.get_single_message(message_id)
    message.update(data)
    message_data = message_schema.dump(message)
    return custom_response(message_data, 201)

@message_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    req_data = request.get_json()
    data = message_schema.load(req_data)
    content = data.get('content')
    if not content:
        message = {'error': 'Message cannot be empty'}
        return custom_response(message, 400)
    message = MessageModel(data)
    message.save()
    data = message_schema.dump(message)
    return custom_response(data, 201)

@message_api.route('/', methods=['GET'])
@Auth.auth_required
def get_users_messages(): 
    messages = MessageModel.get_users_messages(Auth.current_user_id())

    if len(messages) < 1:
        return custom_response({'error': 'You have no previous messages'}, 400)

    data = message_schema.dump(messages, many=True)
    return custom_response(data, 200)
