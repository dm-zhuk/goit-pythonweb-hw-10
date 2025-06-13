import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from redis.asyncio import Redis
from dotenv import load_dotenv

from src.settings.base import settings
from src.routers import contacts, users
from src.routers import utils

load_dotenv()
app = FastAPI(title="Contacts API", description="Contacts management REST API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("BASE_URL")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Rate limiting
@app.on_event("startup")
async def startup():
    redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)
    await FastAPILimiter.init(redis)


app.include_router(utils.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(users.router, prefix="/api")


# docker-compose down
# export COMPOSE_BAKE=true
# docker-compose build --no-cache
# docker-compose up -d
# docker-compose exec web ls -l /app/src/services/templates

# poetry run uvicorn src.main:app --reload --log-level debug
# curl -X POST http://localhost:8000/users/request_email \-H "Content-Type: application/json" \-d '{"email": "user@example.com"}'

# curl -X POST http://0.0.0.0:8000/contacts/ -H "Content-Type: application/json" -d '{"first_name":"Kim","last_name":"Philby","email":"kimf@mail.co.uk","phone_number":"012223456789","birthday":"1985-05-06,"additional_data": "test-02"}'

# python del_pycache.py

# openssl rand -hex 32 (create JWT_SECRET)
