from dotenv import load_dotenv
import os
import requests
from pymongo import MongoClient

# Database connection configuration
client = MongoClient("mongodb+srv://ricardokneri:Kb1LujGFHzYZz6dT@cluster0.hso0g.mongodb.net/")
db = client["my_database"]
collection = db["Fixtures_2024"]

# Load environment variables
load_dotenv()
api_key = os.getenv('API_KEY')
if not api_key:
    raise ValueError("API_KEY is not set in the environment variables.")

headers = {
    "x-rapidapi-key": api_key,
    "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}


def fetch_teams():
    """
    Fetch Premier League teams for the 2023 season.
    Returns a dictionary mapping team names to their IDs.
    """
    url = "https://api-football-v1.p.rapidapi.com/v3/teams?league=39&season=2024"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        teams = response.json().get('response', [])
        # Convert list of teams into a dictionary mapping names to IDs
        return {team['team']['name'].lower(): team['team']['id'] for team in teams}
    else:
        print(f"Failed to fetch teams: {response.status_code} - {response.text}")
        return {}

def get_team_id_by_name(team_name):
    """
    Get the team ID for the given team name.
    Parameters:
        team_name (str): Name of the team (case insensitive).
    Returns:
        int: Team ID if found.
    """
    teams_info = fetch_teams()
    team_id = teams_info.get(team_name.lower())
    if team_id:
        return team_id
    else:
        raise ValueError(f"Team '{team_name}' not found in the fetched data.")
    

def fetch_fixtures_for_team(team_id):
    """
    Fetch fixtures for a given team and season 2024.
    Returns a list of fixture data.
    """
    url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures?team={team_id}&season=2024"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('response', [])
    else:
        print(f"Failed to fetch fixtures for team {team_id}: {response.status_code} - {response.text}")
        return []

def fetch_fixture_statistics(fixture_id):
    """
    Fetch statistics for a given fixture.
    Returns a list of statistics data.
    """
    url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures/statistics?fixture={fixture_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('response', [])
    else:
        print(f"Failed to fetch statistics for fixture {fixture_id}: {response.status_code} - {response.text}")
        return []

def populate_database(collection):
    """
    Populate the MongoDB database with Premier League team fixtures and statistics for the 2024 season.
    """
    teams_info = fetch_teams()
    if not teams_info:
        print("No teams data fetched. Exiting populate_database.")
        return

    for team_name, team_id in teams_info.items():
        print(f"Processing team: {team_name} (ID: {team_id})")
        fixtures = fetch_fixtures_for_team(team_id)
        if not fixtures:
            print(f"No fixtures found for team {team_name}. Skipping...")
            continue

        for fixture in fixtures:
            if 'fixture' not in fixture or 'id' not in fixture['fixture']:
                print(f"Invalid fixture format: {fixture}. Skipping...")
                continue

            fixture_id = fixture['fixture']['id']
            stats = fetch_fixture_statistics(fixture_id)
            if stats:
                fixture['statistics'] = stats
            else:
                print(f"No statistics found for fixture {fixture_id}. Skipping...")

        document = {
            "team_id": team_id,
            "team_name": team_name,
            "season": 2024,
            "fixtures": fixtures
        }

        collection.update_one(
            {"team_id": team_id, "season": 2024},
            {"$set": document},
            upsert=True
        )
        print(f"Data for team {team_name} successfully updated.")
