from time import perf_counter

from app.db.neo4j_client import neo4j_client


class PerformanceService:
    @staticmethod
    def create_indexes():
        queries = [
            "CREATE INDEX user_id_index IF NOT EXISTS FOR (u:User) ON (u.id)",
            "CREATE INDEX game_id_index IF NOT EXISTS FOR (g:Game) ON (g.id)",
            "CREATE INDEX genre_name_index IF NOT EXISTS FOR (g:Genre) ON (g.name)",
            "CREATE INDEX platform_name_index IF NOT EXISTS FOR (p:Platform) ON (p.name)"
        ]

        for query in queries:
            neo4j_client.execute_write(query)

        return {"message": "Indexes created successfully"}

    @staticmethod
    def run_performance_test(user_id: str = "user_1", game_id: str = "game_1"):
        tests = [
            {
                "name": "Find user by id",
                "query": "MATCH (u:User {id: $user_id}) RETURN u",
                "parameters": {"user_id": user_id}
            },
            {
                "name": "Find game by id",
                "query": "MATCH (g:Game {id: $game_id}) RETURN g",
                "parameters": {"game_id": game_id}
            },
            {
                "name": "Recommendations by genre",
                "query": """
                MATCH (u:User {id: $user_id})-[:LIKED]->(:Game)-[:HAS_GENRE]->(genre:Genre)
                MATCH (recommended:Game)-[:HAS_GENRE]->(genre)
                WHERE NOT (u)-[:LIKED]->(recommended)
                RETURN recommended.title AS title, count(genre) AS score
                ORDER BY score DESC
                LIMIT 10
                """,
                "parameters": {"user_id": user_id}
            },
            {
                "name": "Similar users",
                "query": """
                MATCH (u1:User {id: $user_id})-[:LIKED]->(g:Game)<-[:LIKED]-(u2:User)
                WHERE u1 <> u2
                RETURN u2.username AS username, count(g) AS common_likes
                ORDER BY common_likes DESC
                LIMIT 10
                """,
                "parameters": {"user_id": user_id}
            }
        ]

        results = []

        for test in tests:
            start = perf_counter()
            records = neo4j_client.execute_read(test["query"], test["parameters"])
            end = perf_counter()

            results.append(
                {
                    "name": test["name"],
                    "execution_time_ms": round((end - start) * 1000, 3),
                    "returned_records": len(records)
                }
            )

        return results
