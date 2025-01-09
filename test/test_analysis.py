import unittest
from unittest.mock import MagicMock
from my_package import getMatches

class TestAnalysis(unittest.TestCase):
    def test_get_matches(self):
        mock_collection = MagicMock()
        mock_collection.aggregate.return_value = [
            {
                "winsHome": [{"winHome": [1, 2]}],
                "winsAway": [{"winAway": [3]}],
                "lossHome": [{"lossHome": [4]}],
                "lossAway": [{"lossAway": [5]}],
            }
        ]
        stats = getMatches(mock_collection, team_id=1)
        self.assertEqual(stats["Wins Home"], 2)
        self.assertEqual(stats["Losses Away"], 1)

if __name__ == "__main__":
    unittest.main()
