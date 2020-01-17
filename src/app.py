from flask_cors import CORS
from flask import Flask, render_template
from .config import app_config
from .models import db, bcrypt
from .models import PlayerModel
from .models import GameModel
from .models import ResultModel
from .models import MessageModel
from .models import PhotoModel
from .models import SportModel
from .views.PhotoView import photo_api as photo_blueprint
from .views.ResultView import result_api as result_blueprint
from .views.PlayerView import player_api as player_blueprint
from .views.MessageView import message_api as message_blueprint
from .views.GameView import game_api as game_blueprint
from .views.SportView import sport_api as sport_blueprint

def create_app(env_name):
    # app initiliazation
    app = Flask(__name__)

    cors = CORS(app)

    app.config.from_object(app_config[env_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CORS_HEADERS'] = 'Content-Type'

    bcrypt.init_app(app)

    db.init_app(app)

    app.register_blueprint(game_blueprint, url_prefix='/api/v1/games')
    app.register_blueprint(result_blueprint, url_prefix='/api/v1/results')
    app.register_blueprint(player_blueprint, url_prefix='/api/v1/players')
    app.register_blueprint(message_blueprint, url_prefix='/api/v1/messages')
    app.register_blueprint(photo_blueprint, url_prefix='/api/v1/photos')
    app.register_blueprint(sport_blueprint, url_prefix='/api/v1/sports')

    return app
