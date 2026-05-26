from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.config import runtime_config
from app.db.neo4j_client import neo4j_client


@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    yield
    neo4j_client.close()


app = FastAPI(
    title="Neo4j Game Recommender",
    description="Sistem de recomandare pentru jocuri video folosind Neo4j si FastAPI",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
def root():
    return {
        "message": "Neo4j Game Recommender API",
        "docs": "/docs"
    }


if __name__ == "__main__":
    uvicorn.run("app.main:app", host=runtime_config.api_host, port=runtime_config.api_port, reload=True)
