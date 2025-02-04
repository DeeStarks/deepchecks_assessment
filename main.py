from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from infrastructure.container import Container
from infrastructure.handlers import Handlers

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.container = Container()
for handler in Handlers.iterator():
    app.include_router(handler.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=settings.web_port)
