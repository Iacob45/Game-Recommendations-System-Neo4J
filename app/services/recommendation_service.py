from app.db.neo4j_client import neo4j_client


class RecommendationService:
    @staticmethod
    def get_recommendations_for_user(user_id: str, limit: int = 10):
        query = """
        MATCH (u:User {id: $user_id})-[:LIKED]->(:Game)-[:HAS_GENRE]->(genre:Genre)
        MATCH (recommended:Game)-[:HAS_GENRE]->(genre)
        WHERE NOT (u)-[:LIKED]->(recommended)
          AND NOT (u)-[:PLAYED]->(recommended)

        OPTIONAL MATCH (recommended)-[:HAS_GENRE]->(allGenre:Genre)
        WITH recommended, count(DISTINCT genre) AS score, collect(DISTINCT allGenre.name) AS genres

        OPTIONAL MATCH (recommended)-[:AVAILABLE_ON]->(platform:Platform)
        WITH recommended, score, genres, collect(DISTINCT platform.name) AS platforms

        OPTIONAL MATCH (recommended)-[:DEVELOPED_BY]->(developer:Developer)
        OPTIONAL MATCH (recommended)-[:PUBLISHED_BY]->(publisher:Publisher)

        RETURN recommended {
            .id,
            .title,
            .release_year,
            genres: genres,
            platforms: platforms,
            developer: developer.name,
            publisher: publisher.name
        } AS game,
        score
        ORDER BY score DESC, game.title
        LIMIT $limit
        """

        result = neo4j_client.execute_read(query, {"user_id": user_id, "limit": limit})
        return result

    @staticmethod
    def get_similar_users(user_id: str, limit: int = 10):
        query = """
        MATCH (u1:User {id: $user_id})-[:LIKED]->(g:Game)<-[:LIKED]-(u2:User)
        WHERE u1 <> u2
        RETURN u2 {
            .id,
            .username,
            .age
        } AS user,
        count(g) AS common_likes
        ORDER BY common_likes DESC, user.username
        LIMIT $limit
        """

        result = neo4j_client.execute_read(query, {"user_id": user_id, "limit": limit})
        return result

    @staticmethod
    def get_similar_games(game_id: str, limit: int = 10):
        query = """
        MATCH (g1:Game {id: $game_id})-[:HAS_GENRE]->(genre:Genre)<-[:HAS_GENRE]-(g2:Game)
        WHERE g1 <> g2

        OPTIONAL MATCH (g2)-[:HAS_GENRE]->(allGenre:Genre)
        WITH g2, count(DISTINCT genre) AS score, collect(DISTINCT allGenre.name) AS genres

        OPTIONAL MATCH (g2)-[:AVAILABLE_ON]->(platform:Platform)
        WITH g2, score, genres, collect(DISTINCT platform.name) AS platforms

        OPTIONAL MATCH (g2)-[:DEVELOPED_BY]->(developer:Developer)
        OPTIONAL MATCH (g2)-[:PUBLISHED_BY]->(publisher:Publisher)

        RETURN g2 {
            .id,
            .title,
            .release_year,
            genres: genres,
            platforms: platforms,
            developer: developer.name,
            publisher: publisher.name
        } AS game,
        score
        ORDER BY score DESC, game.title
        LIMIT $limit
        """

        result = neo4j_client.execute_read(query, {"game_id": game_id, "limit": limit})
        return result
