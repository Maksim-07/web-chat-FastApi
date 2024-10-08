import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.config import settings

app = FastAPI(
    title="Web Chat",
    openapi_url="/api/openapi.json",
    docs_url="/api/swagger",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host=settings().server_host, port=settings().server_port)
