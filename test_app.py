from unittest import TestCase

from app import app, games

from boggle import BoggleGame

import json

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<!-- boggle board -->', html)
            # test that you're getting a template

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            # Getting POST response
            response = client.post('/api/new-game')

            # Since we want JSON, we convert the response to JSON
            json = response.get_json()

            # Testing the structure, we care about the type
            # Since value of gameId will always change, we can just test that it will always be a string
            self.assertTrue(type(json["gameId"]) == type(""))
            # Checking that the value of "board" will always be instance of list
            self.assertIsInstance(json["board"], list)
            # Checking to see that the value of "gameId" is in games
            self.assertIn(json["gameId"], games)

    def test_score_word(self):
        """Test checking if a word is on the board or in wordlist."""

        with self.client as client:
            response = client.post('/api/new-game')
            json = response.get_json()
            id = json["gameId"]

            games[json["gameId"]].board = [
                ['A', 'P', 'P', 'L', 'E'],
                ['Z', 'Z', 'Z', 'L', 'E'],
                ['Z', 'Z', 'Z', 'L', 'E'],
                ['Z', 'Z', 'Z', 'L', 'E'],
                ['Z', 'Z', 'Z', 'L', 'E']]

            response = client.post('/api/score-word', json={"gameId": id, "word": "APPLE"})
            json = response.get_json()
            self.assertEqual(json["result"], "ok")

            response = client.post('/api/score-word', json={"gameId": id, "word": "HELLO"})
            json = response.get_json()
            self.assertEqual(json["result"], "not-on-board")

            response = client.post('/api/score-word', json={"gameId": id, "word": "LASJKD"})
            json = response.get_json()
            self.assertEqual(json["result"], "not-word")



