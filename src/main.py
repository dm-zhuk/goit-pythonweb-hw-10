from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter

from src.database.connect import init_db, client
from src.utils import compute_value
from src.services.base import settings
from src.routers import contacts, users, utils

import uvicorn

app = FastAPI(title="Contacts API", description="Contacts management REST API")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.BASE_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await init_db()
    await FastAPILimiter.init(client)


@app.get("/compute/{value}")
async def get_computed_value(value: int):
    result = compute_value(value)
    return {"result": result}


app.include_router(utils.router, prefix="/api")
app.include_router(contacts.router, prefix="/api/contacts")
app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run("src.main:app", debug=True, reload=True)
