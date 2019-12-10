import unittest
import os
import json
from ..app import create_app, db
from ..models.PostModel import PostModel, PostSchema

class PostTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app("test")
        self.client = self.app.test_client

        self.player_1 = {
          "first_name": "Dom",
          "last_name": "T",
          "email": "dom@test.com",
          "password": "password",
          "gender": "M",
          "dob": "1990-01-01",
          "ability": "Beginner",
          "postcode": "N169NP"
        }

        self.player_2 = {
          "first_name": "Pam",
          "last_name": "M",
          "email": "pam@spam.com",
          "password": "password",
          "gender": "F",
          "dob": "1991-01-01",
          "ability": "Advanced",
          "postcode": "N169NP"
        }

        with self.app.app_context():
          db.create_all()
          player = PlayerModel(self.player_1)
          db.session.add(player)
          db.session.commit()
          db.session.refresh(player)
          player_1_id = player.id
          player2 = PlayerModel(self.player_2)
          db.session.add(player2)
          db.session.commit()
          db.session.refresh(player2)
          player_2_id = player2.id

        self.post_1 = {
          'content': 'This is a post'
        }

    def test_create_post(self):
        res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player_1))
        api_token = json.loads(res.data).get('jwt_token')
        res = self.client().post('api/v1/messages/', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(self.post_1))
        json_data = json.loads(res.data)
        self.assertEqual(json_data.get('player_id'), 1)
        self.assertEqual(json_data.get('content'), 'This is a post')

    def tearDown(self):
       """
       Runs at the end of the test case; drops the db
       """
       with self.app.app_context():
         db.session.remove()
         db.drop_all()

if __name__ == "__main__":
    unittest.main()
