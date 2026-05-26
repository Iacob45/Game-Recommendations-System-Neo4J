import os
from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeConfig:
    neo4j_uri: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    neo4j_username: str = os.getenv("NEO4J_USERNAME", "neo4j")
    neo4j_password: str = os.getenv("NEO4J_PASSWORD", "password123")
    neo4j_database: str = os.getenv("NEO4J_DATABASE", "neo4j")
    api_host: str = os.getenv("API_HOST", "127.0.0.1")
    api_port: int = int(os.getenv("API_PORT", "8000"))


runtime_config = RuntimeConfig()
