from neo4j import GraphDatabase

from app.config import runtime_config


class Neo4jClient:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            runtime_config.neo4j_uri,
            auth=(runtime_config.neo4j_username, runtime_config.neo4j_password)
        )
        self.database = runtime_config.neo4j_database

    def close(self):
        self.driver.close()

    def execute_read(self, query: str, parameters: dict | None = None):
        parameters = parameters or {}

        with self.driver.session(database=self.database) as session:
            result = session.execute_read(self._run_query, query, parameters)
            return result

    def execute_write(self, query: str, parameters: dict | None = None):
        parameters = parameters or {}

        with self.driver.session(database=self.database) as session:
            result = session.execute_write(self._run_query, query, parameters)
            return result

    @staticmethod
    def _run_query(tx, query: str, parameters: dict):
        result = tx.run(query, parameters)
        return [record.data() for record in result]


neo4j_client = Neo4jClient()
