import unittest
from unittest.mock import patch
from my_package import fetch_teams, fetch_fixtures_for_team

class TestETLPipeline(unittest.TestCase):
    @patch("etl_pipeline.requests.get")
    def test_fetch_teams(self, mock_get):
        mock_get.return_value.json.return_value = {
            "response": [{"team": {"id": 1, "name": "Team A"}}]
        }
        teams = fetch_teams()
        self.assertEqual(teams["team a"], 1)

    @patch("etl_pipeline.requests.get")
    def test_fetch_fixtures_for_team(self, mock_get):
        mock_get.return_value.json.return_value = {
            "response": [{"fixture": {"id": 1}, "teams": {"home": {}, "away": {}}}]
        }
        fixtures = fetch_fixtures_for_team(1)
        self.assertEqual(len(fixtures), 1)

if __name__ == "__main__":
    unittest.main()
