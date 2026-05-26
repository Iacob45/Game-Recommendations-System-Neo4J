from app.db.neo4j_client import neo4j_client


class StatisticsService:
    @staticmethod
    def get_statistics():
        query = """
        MATCH (u:User)
        WITH count(u) AS total_users

        MATCH (g:Game)
        WITH total_users, count(g) AS total_games

        MATCH (genre:Genre)
        WITH total_users, total_games, count(genre) AS total_genres

        MATCH (platform:Platform)
        WITH total_users, total_games, total_genres, count(platform) AS total_platforms

        MATCH ()-[r]->()
        WITH
            total_users,
            total_games,
            total_genres,
            total_platforms,
            type(r) AS relationship_type,
            count(r) AS total
        ORDER BY total DESC

        WITH
            total_users,
            total_games,
            total_genres,
            total_platforms,
            collect({
                type: relationship_type,
                total: total
            }) AS relationships

        RETURN {
            total_users: total_users,
            total_games: total_games,
            total_genres: total_genres,
            total_platforms: total_platforms,
            relationships: relationships
        } AS statistics
        """

        result = neo4j_client.execute_read(query)
        return result[0]["statistics"] if result else {}

    @staticmethod
    def get_games_by_genre():
        query = """
        MATCH (g:Game)-[:HAS_GENRE]->(genre:Genre)
        RETURN genre.name AS genre, count(g) AS total_games
        ORDER BY total_games DESC, genre
        """

        return neo4j_client.execute_read(query)
