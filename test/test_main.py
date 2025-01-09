import unittest
from unittest.mock import patch
from my_package import main

class TestMain(unittest.TestCase):
    @patch("builtins.input", side_effect=["yes", "Manchester United"])
    @patch("main.populate_database")
    @patch("main.getMatches")
    def test_main_workflow(self, mock_get_matches, mock_populate_db, mock_input):
        mock_get_matches.return_value = {
            "Wins Home": 10, "Wins Away": 7, "Losses Home": 3, "Losses Away": 5
        }
        mock_populate_db.return_value = None

        with patch("main.plot_home_away_performance") as mock_plot:
            with patch("main.plot_goals_trend"):
                main()
                mock_populate_db.assert_called_once()
                mock_get_matches.assert_called_once()
                mock_plot.assert_called_once()

if __name__ == "__main__":
    unittest.main()
