import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from api.api_user import router
from core.config import settings

app = FastAPI(
    title="web-chat",
    openapi_url="/api/openapi.json",
    docs_url="/api/swagger",
)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def redirect_to_auth():
    return RedirectResponse(url="/auth")


@app.get("/chat")
async def redirect_to_auth():
    return {"login": True}


if __name__ == "__main__":
    uvicorn.run(app, host=settings().server_host, port=settings().server_port)
