import matplotlib.pyplot as plt


def build_outcome_pipeline(team_id):
    """
    Dynamically builds the aggregation pipeline for MongoDB queries.

    Parameters:
    - team_id: The ID of the team to filter data for

    Returns:
    - List representing the aggregation pipeline
    """
    return [
        {"$unwind": "$fixtures"},  # Unwind the fixtures array
        {"$facet": {  # Splits the pipeline to gather separate data
            "winsHome": [
                {"$match": {
                    "$or": [
                        {"fixtures.teams.home.winner": True, "fixtures.teams.home.id": team_id}  # Collects Wins
                    ]
                }},
                {"$group": {
                    "_id": None,
                    "winHome": {"$addToSet": "$fixtures.fixture.id"}  # Creates a set of unique fixture ids
                }}
            ],
            "winsAway": [
                {"$match": {
                    "$or": [
                        {"fixtures.teams.away.winner": True, "fixtures.teams.away.id": team_id}  # Collects Wins
                    ]
                }},
                {"$group": {
                    "_id": None,
                    "winAway": {"$addToSet": "$fixtures.fixture.id"}
                }}
            ],
            "lossHome": [
                {"$match": {
                    "$or": [
                        {"fixtures.teams.home.winner": False, "fixtures.teams.home.id": team_id}  # Collects Losses
                    ]
                }},
                {"$group": {
                    "_id": None,
                    "lossHome": {"$addToSet": "$fixtures.fixture.id"}
                }}
            ],
            "lossAway": [
                {"$match": {
                    "$or": [
                        {"fixtures.teams.away.winner": False, "fixtures.teams.away.id": team_id}  # Collects Losses
                    ]
                }},
                {"$group": {
                    "_id": None,
                    "lossAway": {"$addToSet": "$fixtures.fixture.id"}
                }}
            ],
        }}
    ]


def getMatches(collection, team_id):
    """
    Executes the dynamically built aggregation pipeline and prints win/loss statistics.

    Parameters:
    - collection: MongoDB collection object
    - team_id: ID of the team to analyze

    Returns:
    - Dictionary with win/loss statistics
    """
    # Build the pipeline dynamically for the given team_id
    pipeline = build_outcome_pipeline(team_id)

    # Execute the pipeline
    results = collection.aggregate(pipeline)

    # Extract results
    stats = {}
    for result in results:
        stats["Wins Home"] = len(result.get("winsHome", [])[0].get("winHome", [])) if result.get("winsHome") else 0
        stats["Wins Away"] = len(result.get("winsAway", [])[0].get("winAway", [])) if result.get("winsAway") else 0
        stats["Losses Home"] = len(result.get("lossHome", [])[0].get("lossHome", [])) if result.get("lossHome") else 0
        stats["Losses Away"] = len(result.get("lossAway", [])[0].get("lossAway", [])) if result.get("lossAway") else 0

    return stats


def getGoals(cursor):
    """
    Extracts the goals scored by a specific team from the MongoDB cursor.

    Parameters:
    - cursor: MongoDB cursor object containing match data

    Returns:
    - List of goals scored by the team in each match
    """
    home_goals = []
    away_goals = []

    for doc in cursor:
        for fixture in doc.get('fixtures', []):
            home_team = fixture.get("teams", {}).get("home", {}).get("id", {})
            away_team = fixture.get("teams", {}).get("away", {}).get("id", {})
            home_goal = fixture.get("goals", {}).get("home", 0)
            away_goal = fixture.get("goals", {}).get("away", 0)

            if home_team == 33 and home_goal is not None:
                home_goals.append(home_goal)
            elif away_team == 33 and away_goal is not None: 
                away_goals.append(away_goal)

    return home_goals + away_goals  # Combine home and away goals



# Assuming `getGoals(cursor)` retrieves the goals data
def plot_goals_trend(cursor):
    """
    Plots the trend of goals scored during the 2024 season.

    Parameters:
    - cursor: Database cursor to retrieve the goals data

    Returns:
    None
    """
    # Fetch goals data
    goals = getGoals(cursor)
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(goals, marker='o', linestyle='-', color='blue', label='Goals per Match')
    
    # Add labels, title, and grid
    plt.title("Goals Scored Per Match in Season 2024", fontsize=14)
    plt.xlabel("Match Number", fontsize=12)
    plt.ylabel("Goals Scored", fontsize=12)
    plt.grid(visible=True, linestyle='--', alpha=0.7)
    
    # Add legend
    plt.legend(loc='upper left', fontsize=10)
    
    # Display the plot
    plt.tight_layout()
    plt.show()


def plot_home_away_performance(stats):
    """
    Plots home vs. away performance based on win/loss statistics.

    Parameters:
    - stats: Dictionary containing win/loss statistics

    Returns:
    None
    """
    # Prepare data for plotting
    categories = ["Wins", "Losses"]
    home_data = [stats["Wins Home"], stats["Losses Home"]]
    away_data = [stats["Wins Away"], stats["Losses Away"]]

    # Plot the data
    x = range(len(categories))  # Create x-axis positions
    bar_width = 0.4  # Width of the bars

    plt.figure(figsize=(8, 5))
    plt.bar(x, home_data, width=bar_width, label="Home", color="blue")
    plt.bar([i + bar_width for i in x], away_data, width=bar_width, label="Away", color="orange")

    # Add labels, title, and legend
    plt.title("Home vs. Away Performance", fontsize=14)
    plt.xlabel("Category", fontsize=12)
    plt.ylabel("Count", fontsize=12)
    plt.xticks([i + bar_width / 2 for i in x], categories)  # Center the category labels
    plt.legend(loc="upper left", fontsize=10)

    # Display the plot
    plt.tight_layout()
    plt.show()