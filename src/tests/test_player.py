import unittest
import os
import json
from ..app import create_app, db
from ..models.PlayerModel import PlayerModel, PlayerSchema
from .helper import PLAYER_1, PLAYER_2

class PlayersTest(unittest.TestCase):
  
  def setUp(self):
    self.app = create_app("test")
    self.client = self.app.test_client
    self.player = PLAYER_1
    self.player2 = PLAYER_2
    with self.app.app_context():
        db.create_all()
        player2 = PlayerModel(self.player2)
        db.session.add(player2)
        db.session.commit()
        db.session.refresh(player2)
        player2_id = player2.id

  def test_player_created(self):
    res = self.client().post('api/v1/players/new', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player))
    json_data = json.loads(res.data)
    self.assertTrue(json_data.get('jwt_token'))
    self.assertEqual(res.status_code, 201)

  def test_error_when_existing_email_used_to_create_account(self):
    res = self.client().post('api/v1/players/new', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player))
    self.assertEqual(res.status_code, 201)
    res = self.client().post('api/v1/players/new', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error'), 'Player already exist, please supply another email address')

  def test_player_login(self):
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player2))
    json_data = json.loads(res.data)
    self.assertTrue(json_data.get('jwt_token'))
    self.assertEqual(res.status_code, 200)

  def test_error_when_player_login_with_invalid_password(self):
    invalid_password_player = {
      "email": "pam@test.com",
      "password": "dgfdgdfg!"
    }
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(invalid_password_player))
    json_data = json.loads(res.data)
    self.assertFalse(json_data.get('jwt_token'))
    self.assertEqual(json_data.get('error'), 'The password that you have submitted is invalid.  Please try again.')
    self.assertEqual(res.status_code, 400)

  def test_error_when_player_login_with_invalid_email(self):
    invalid_email_player = {
      "email": "bob@te.com",
      "password": "password"
    }
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(invalid_email_player))
    json_data = json.loads(res.data)
    self.assertEqual(json_data.get('error'), 'An account by this email address does not exist.  Please check that you have entered the correct email or create a new account')
    self.assertFalse(json_data.get('jwt_token'))
    self.assertEqual(res.status_code, 400)

  def test_error_user_logs_in_without_email(self):
    incomplete_player = {
      "password": "password"
    }
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(incomplete_player))
    json_data = json.loads(res.data)
    self.assertEqual(json_data.get('error'), 'Please enter both your email and password to continue')
    self.assertFalse(json_data.get('jwt_token'))
    self.assertEqual(res.status_code, 400)

  def test_player_can_view_their_own_profile(self):
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player2))
    api_token = json.loads(res.data).get('jwt_token')
    res = self.client().get('api/v1/players/my_profile', headers={'Content-Type': 'application/json', 'api-token': api_token})
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(json_data.get('email'), 'pam@test.com')
    self.assertEqual(json_data.get('first_name'), 'Pam')

  def test_player_can_update_their_name(self):
    updated_name = {
      "first_name": "Pammy"
    }
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player2))
    api_token = json.loads(res.data).get('jwt_token')
    res = self.client().patch('api/v1/players/my_profile', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(updated_name))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(json_data.get('email'), 'pam@test.com')
    self.assertEqual(json_data.get('first_name'), 'Pammy')

  def test_player_can_update_their_password(self):
    updated_player = {
      "password": "password2",
      "gender": "Male"
    }
    res = self.client().post('api/v1/players/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.player2))
    api_token = json.loads(res.data).get('jwt_token')
    res = self.client().patch('api/v1/players/my_profile', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(updated_player))
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    print(json_data)
    self.assertEqual(json_data.get('email'), 'pam@test.com')
    self.assertEqual(json_data.get('gender'), 'Male')

  def test_haversine_distances(self):
    self.assertEqual(PlayerModel.get_distance_between_postcodes([[51.5255534, -0.0268686]], [[51.5255534, -0.0268686]]), 0)

  def test_player_location(self):
    self.assertEqual(PlayerModel.get_player_location("N65HQ"), "Haringey")

  def tearDown(self):
    with self.app.app_context():
      db.session.remove()
      db.drop_all()

if __name__ == "__main__":
  unittest.main()