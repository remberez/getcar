import uvicorn
from fastapi import FastAPI

from config import settings
from endpoints import router

app = FastAPI()
app.include_router(router=router)


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        reload=settings.server_reload,
        host=settings.server_host,
        port=settings.server_port,
    )
