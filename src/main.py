from fastapi import FastAPI

from src.config import settings
from src.database import Base, engine
from src.tasks.router import router as tasks_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

Base.metadata.create_all(bind=engine)

app.include_router(tasks_router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "app": settings.APP_NAME}
