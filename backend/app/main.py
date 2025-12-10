from fastapi import FastAPI

from app.api.v1.planning import router as planning_router

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(planning_router, prefix="/api/v1")