import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.router import router
from api.static import router as static_router
from core.config import settings

app = FastAPI(
    title="web-chat",
    openapi_url="/api/openapi.json",
    docs_url="/api/swagger",
)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(static_router)
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host=settings().SERVER_HOST, port=settings().SERVER_PORT)
