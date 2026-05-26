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
