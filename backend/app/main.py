from fastapi import FastAPI

from app.routers.notes import router as notes_router

app = FastAPI(title="CapIAbara API", version="0.1.0")

app.include_router(notes_router)


@app.get("/")
def root():
    return {"status": "ok", "service": "capiabara"}
