from flask import request, Blueprint
from ..shared.Authentication import Auth
from ..models.ConversationModel import ConversationModel, ConversationSchema
from .helpers import custom_response

conversation_api = Blueprint('conversation_api', __name__)
conversation_schema = ConversationSchema()


@conversation_api.route('/', methods=['GET'])
@Auth.auth_required
def get_conversations():
    user_id = Auth.current_user_id()
    conversation = ConversationModel.get_conversations(user_id).first()
    if not conversation:
        message = {"Error": "No Previous Conversations"}
        return custom_response(message, 400)

    conversations = ConversationModel.get_conversations(user_id)
    data = conversation_schema.dump(conversations, many=True)
    return custom_response(data, 200)
