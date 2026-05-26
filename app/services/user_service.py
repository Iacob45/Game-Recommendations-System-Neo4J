from app.db.neo4j_client import neo4j_client
from app.models.user import UserCreate


class UserService:
    @staticmethod
    def create_user(body: UserCreate):
        query = """
        MERGE (u:User {id: $id})
        SET u.username = $username,
            u.age = $age
        RETURN u {
            .id,
            .username,
            .age
        } AS user
        """

        result = neo4j_client.execute_write(query, body.model_dump())
        return result[0]["user"]

    @staticmethod
    def get_users():
        query = """
        MATCH (u:User)
        RETURN u {
            .id,
            .username,
            .age
        } AS user
        ORDER BY u.username
        """

        result = neo4j_client.execute_read(query)
        return [record["user"] for record in result]

    @staticmethod
    def get_user_by_id(user_id: str):
        query = """
        MATCH (u:User {id: $user_id})
        RETURN u {
            .id,
            .username,
            .age
        } AS user
        """

        result = neo4j_client.execute_read(query, {"user_id": user_id})
        return result[0]["user"] if result else None

    @staticmethod
    def play_game(user_id: str, game_id: str):
        query = """
        MATCH (u:User {id: $user_id})
        MATCH (g:Game {id: $game_id})
        MERGE (u)-[:PLAYED]->(g)
        RETURN u.id AS user_id, g.id AS game_id
        """

        result = neo4j_client.execute_write(query, {"user_id": user_id, "game_id": game_id})
        return result[0] if result else None

    @staticmethod
    def like_game(user_id: str, game_id: str):
        query = """
        MATCH (u:User {id: $user_id})
        MATCH (g:Game {id: $game_id})
        MERGE (u)-[:LIKED]->(g)
        RETURN u.id AS user_id, g.id AS game_id
        """

        result = neo4j_client.execute_write(query, {"user_id": user_id, "game_id": game_id})
        return result[0] if result else None

    @staticmethod
    def rate_game(user_id: str, game_id: str, score: int):
        query = """
        MATCH (u:User {id: $user_id})
        MATCH (g:Game {id: $game_id})
        MERGE (u)-[r:RATED]->(g)
        SET r.score = $score
        RETURN u.id AS user_id, g.id AS game_id, r.score AS score
        """

        result = neo4j_client.execute_write(
            query,
            {
                "user_id": user_id,
                "game_id": game_id,
                "score": score
            }
        )
        return result[0] if result else None
