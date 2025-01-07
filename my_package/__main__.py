from pymongo import MongoClient
from etl_pipeline import populate_database, get_team_id_by_name
from analysis import getGoals, getMatches, plot_goals_trend, plot_home_away_performance

def main():
    """
    Main function to manage database interactions and call analysis functions.
    """
    print("Starting Project")
    
    # Database connection
    client = MongoClient("mongodb+srv://ricardokneri:Kb1LujGFHzYZz6dT@cluster0.hso0g.mongodb.net/")
    db = client["my_database"]
    collection = db["Fixtures_2024"]

    try:
        # Populate database if needed
        if input("Do you want to populate the database? (yes/no): ").lower() == "yes":
            populate_database(collection)

        # Allow user to input a team name instead of ID
        team_name = input("Enter the team name: ")
        team_id = get_team_id_by_name(team_name)

        # Fetch and print matches
        stats = getMatches(collection, team_id)
        print("Team Performance Statistics:")
        for key, value in stats.items():
            print(f"{key}: {value}")

        # Plot home vs. away performance
        plot_home_away_performance(stats)

        # Fetch and plot goals trend
        cursor = collection.find({"team_id": team_id, "season": 2024})
        plot_goals_trend(cursor)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the database connection
        client.close()

if __name__ == "__main__":
    main()