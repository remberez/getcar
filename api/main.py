import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from config import settings
from endpoints import router

app = FastAPI()
app.include_router(router=router)
app.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost:5173",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/media", StaticFiles(directory="static/media"), name="media")


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        reload=settings.server_reload,
        host=settings.server_host,
        port=settings.server_port,
    )
