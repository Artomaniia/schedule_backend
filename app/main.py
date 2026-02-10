import os
from dotenv import load_dotenv
from fastapi import FastAPI

from .routers import teachers, disciplines, weekdays

load_dotenv()

app = FastAPI(
    title=os.getenv("APP_NAME", "Schedule Backend"),
    version="1.0.0",
)

app.include_router(disciplines.router)
app.include_router(teachers.router)
app.include_router(weekdays.router)


@app.get("/health")
def health():
    return {"status": "ok"}
