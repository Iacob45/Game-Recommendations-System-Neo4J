from app.db.neo4j_client import neo4j_client
from app.services.performance_service import PerformanceService


def clear_database():
    query = "MATCH (n) DETACH DELETE n"
    neo4j_client.execute_write(query)


def seed_users():
    users = [
        {"id": "user_1", "username": "andrei", "age": 23},
        {"id": "user_2", "username": "maria", "age": 22},
        {"id": "user_3", "username": "alex", "age": 24},
        {"id": "user_4", "username": "ioana", "age": 21},
        {"id": "user_5", "username": "vlad", "age": 25}
    ]

    query = """
    UNWIND $users AS user
    MERGE (u:User {id: user.id})
    SET u.username = user.username,
        u.age = user.age
    """

    neo4j_client.execute_write(query, {"users": users})


def seed_games():
    games = [
        {
            "id": "game_1",
            "title": "Elden Ring",
            "release_year": 2022,
            "genres": ["RPG", "Soulslike", "Open World"],
            "platforms": ["PC", "PlayStation 5", "Xbox Series X"],
            "developer": "FromSoftware",
            "publisher": "Bandai Namco"
        },
        {
            "id": "game_2",
            "title": "Dark Souls III",
            "release_year": 2016,
            "genres": ["RPG", "Soulslike"],
            "platforms": ["PC", "PlayStation 4", "Xbox One"],
            "developer": "FromSoftware",
            "publisher": "Bandai Namco"
        },
        {
            "id": "game_3",
            "title": "The Witcher 3",
            "release_year": 2015,
            "genres": ["RPG", "Open World", "Adventure"],
            "platforms": ["PC", "PlayStation 5", "Xbox Series X", "Nintendo Switch"],
            "developer": "CD Projekt Red",
            "publisher": "CD Projekt"
        },
        {
            "id": "game_4",
            "title": "Cyberpunk 2077",
            "release_year": 2020,
            "genres": ["RPG", "Open World", "Action"],
            "platforms": ["PC", "PlayStation 5", "Xbox Series X"],
            "developer": "CD Projekt Red",
            "publisher": "CD Projekt"
        },
        {
            "id": "game_5",
            "title": "God of War",
            "release_year": 2018,
            "genres": ["Action", "Adventure"],
            "platforms": ["PC", "PlayStation 4", "PlayStation 5"],
            "developer": "Santa Monica Studio",
            "publisher": "Sony Interactive Entertainment"
        },
        {
            "id": "game_6",
            "title": "Red Dead Redemption 2",
            "release_year": 2018,
            "genres": ["Open World", "Action", "Adventure"],
            "platforms": ["PC", "PlayStation 4", "Xbox One"],
            "developer": "Rockstar Games",
            "publisher": "Rockstar Games"
        },
        {
            "id": "game_7",
            "title": "GTA V",
            "release_year": 2013,
            "genres": ["Open World", "Action"],
            "platforms": ["PC", "PlayStation 5", "Xbox Series X"],
            "developer": "Rockstar Games",
            "publisher": "Rockstar Games"
        },
        {
            "id": "game_8",
            "title": "Hades",
            "release_year": 2020,
            "genres": ["Roguelike", "Action"],
            "platforms": ["PC", "Nintendo Switch", "PlayStation 5", "Xbox Series X"],
            "developer": "Supergiant Games",
            "publisher": "Supergiant Games"
        },
        {
            "id": "game_9",
            "title": "Stardew Valley",
            "release_year": 2016,
            "genres": ["Simulation", "RPG"],
            "platforms": ["PC", "Nintendo Switch", "PlayStation 4", "Xbox One"],
            "developer": "ConcernedApe",
            "publisher": "ConcernedApe"
        },
        {
            "id": "game_10",
            "title": "Hollow Knight",
            "release_year": 2017,
            "genres": ["Metroidvania", "Action", "Adventure"],
            "platforms": ["PC", "Nintendo Switch", "PlayStation 4", "Xbox One"],
            "developer": "Team Cherry",
            "publisher": "Team Cherry"
        }
    ]

    query = """
    UNWIND $games AS game

    MERGE (g:Game {id: game.id})
    SET g.title = game.title,
        g.release_year = game.release_year

    FOREACH (genreName IN game.genres |
        MERGE (genre:Genre {name: genreName})
        MERGE (g)-[:HAS_GENRE]->(genre)
    )

    FOREACH (platformName IN game.platforms |
        MERGE (platform:Platform {name: platformName})
        MERGE (g)-[:AVAILABLE_ON]->(platform)
    )

    MERGE (developer:Developer {name: game.developer})
    MERGE (g)-[:DEVELOPED_BY]->(developer)

    MERGE (publisher:Publisher {name: game.publisher})
    MERGE (g)-[:PUBLISHED_BY]->(publisher)
    """

    neo4j_client.execute_write(query, {"games": games})


def seed_user_activity():
    activities = [
        {
            "user_id": "user_1",
            "played": ["game_1", "game_2", "game_3"],
            "liked": ["game_1", "game_3"],
            "ratings": [
                {"game_id": "game_1", "score": 10},
                {"game_id": "game_3", "score": 9}
            ]
        },
        {
            "user_id": "user_2",
            "played": ["game_1", "game_2", "game_8"],
            "liked": ["game_1", "game_2", "game_8"],
            "ratings": [
                {"game_id": "game_2", "score": 9},
                {"game_id": "game_8", "score": 10}
            ]
        },
        {
            "user_id": "user_3",
            "played": ["game_3", "game_4", "game_6", "game_7"],
            "liked": ["game_3", "game_6"],
            "ratings": [
                {"game_id": "game_6", "score": 10}
            ]
        },
        {
            "user_id": "user_4",
            "played": ["game_5", "game_6", "game_10"],
            "liked": ["game_5", "game_10"],
            "ratings": [
                {"game_id": "game_5", "score": 8},
                {"game_id": "game_10", "score": 9}
            ]
        },
        {
            "user_id": "user_5",
            "played": ["game_8", "game_9", "game_10"],
            "liked": ["game_8", "game_9"],
            "ratings": [
                {"game_id": "game_9", "score": 9}
            ]
        }
    ]

    query = """
    UNWIND $activities AS activity
    MATCH (u:User {id: activity.user_id})

    FOREACH (gameId IN activity.played |
        MERGE (playedGame:Game {id: gameId})
        MERGE (u)-[:PLAYED]->(playedGame)
    )

    FOREACH (gameId IN activity.liked |
        MERGE (likedGame:Game {id: gameId})
        MERGE (u)-[:LIKED]->(likedGame)
    )

    FOREACH (rating IN activity.ratings |
        MERGE (ratedGame:Game {id: rating.game_id})
        MERGE (u)-[r:RATED]->(ratedGame)
        SET r.score = rating.score
    )
    """

    neo4j_client.execute_write(query, {"activities": activities})


def main():
    print("Clearing database...")
    clear_database()

    print("Creating indexes...")
    PerformanceService.create_indexes()

    print("Seeding users...")
    seed_users()

    print("Seeding games...")
    seed_games()

    print("Seeding user activity...")
    seed_user_activity()

    print("Done.")


if __name__ == "__main__":
    main()
    neo4j_client.close()
