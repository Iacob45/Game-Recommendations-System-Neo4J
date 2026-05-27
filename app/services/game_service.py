from app.db.neo4j_client import neo4j_client
from app.models.game import GameCreate


class GameService:
    @staticmethod
    def create_game(body: GameCreate):
        query = """
        MERGE (g:Game {id: $id})
        SET g.title = $title,
            g.release_year = $release_year

        FOREACH (genreName IN $genres |
            MERGE (genre:Genre {name: genreName})
            MERGE (g)-[:HAS_GENRE]->(genre)
        )

        FOREACH (platformName IN $platforms |
            MERGE (platform:Platform {name: platformName})
            MERGE (g)-[:AVAILABLE_ON]->(platform)
        )

        FOREACH (_ IN CASE WHEN $developer IS NULL THEN [] ELSE [1] END |
            MERGE (developer:Developer {name: $developer})
            MERGE (g)-[:DEVELOPED_BY]->(developer)
        )

        FOREACH (_ IN CASE WHEN $publisher IS NULL THEN [] ELSE [1] END |
            MERGE (publisher:Publisher {name: $publisher})
            MERGE (g)-[:PUBLISHED_BY]->(publisher)
        )

        WITH g
        OPTIONAL MATCH (g)-[:HAS_GENRE]->(genre:Genre)
        WITH g, collect(DISTINCT genre.name) AS genres
        OPTIONAL MATCH (g)-[:AVAILABLE_ON]->(platform:Platform)
        WITH g, genres, collect(DISTINCT platform.name) AS platforms
        OPTIONAL MATCH (g)-[:DEVELOPED_BY]->(developer:Developer)
        OPTIONAL MATCH (g)-[:PUBLISHED_BY]->(publisher:Publisher)

        RETURN g {
            .id,
            .title,
            .release_year,
            genres: genres,
            platforms: platforms,
            developer: developer.name,
            publisher: publisher.name
        } AS game
        """

        result = neo4j_client.execute_write(query, body.model_dump())
        return result[0]["game"]

    @staticmethod
    def get_games():
        query = """
        MATCH (g:Game)
        OPTIONAL MATCH (g)-[:HAS_GENRE]->(genre:Genre)
        WITH g, collect(DISTINCT genre.name) AS genres
        OPTIONAL MATCH (g)-[:AVAILABLE_ON]->(platform:Platform)
        WITH g, genres, collect(DISTINCT platform.name) AS platforms
        OPTIONAL MATCH (g)-[:DEVELOPED_BY]->(developer:Developer)
        OPTIONAL MATCH (g)-[:PUBLISHED_BY]->(publisher:Publisher)

        RETURN g {
            .id,
            .title,
            .release_year,
            genres: genres,
            platforms: platforms,
            developer: developer.name,
            publisher: publisher.name
        } AS game
        ORDER BY g.title
        """

        result = neo4j_client.execute_read(query)
        return [record["game"] for record in result]

    @staticmethod
    def get_game_by_id(game_id: str):
        query = """
        MATCH (g:Game {id: $game_id})
        OPTIONAL MATCH (g)-[:HAS_GENRE]->(genre:Genre)
        WITH g, collect(DISTINCT genre.name) AS genres
        OPTIONAL MATCH (g)-[:AVAILABLE_ON]->(platform:Platform)
        WITH g, genres, collect(DISTINCT platform.name) AS platforms
        OPTIONAL MATCH (g)-[:DEVELOPED_BY]->(developer:Developer)
        OPTIONAL MATCH (g)-[:PUBLISHED_BY]->(publisher:Publisher)

        RETURN g {
            .id,
            .title,
            .release_year,
            genres: genres,
            platforms: platforms,
            developer: developer.name,
            publisher: publisher.name
        } AS game
        """

        result = neo4j_client.execute_read(query, {"game_id": game_id})
        return result[0]["game"] if result else None
