from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from redis.asyncio import Redis

from src.settings.base import settings
from src.routers import contacts, users
from src.api import utils

app = FastAPI(title="Contacts API", description="Contacts management REST API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5050"],
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

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)

# source .venv/bin/activate
# fastapi dev src/main.py
# http://localhost:5050/login?next=/
# http://127.0.0.1:8000/docs


# curl -X POST http://127.0.0.1:8000/contacts/ -H "Content-Type: application/json" -d '{"first_name":"Kim","last_name":"Philby","email":"kimf@mail.co.uk","phone_number":"012223456789","birthday":"1985-05-06,"additional_data": "test-02"}'

# curl -X PUT http://127.0.0.1:8000/contacts/3 -H "Content-Type: application/json" -d '{"first_name":"Kim","last_name":"Philby","email":"kimf@mail.co.uk","phone_number":"01222","birthday":"1985-05-06","additional_data":"test-211(PUT)"}'

# python del_pycache.py


# docker run --name db -e POSTGRES_USER=devops -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=contacts_db -p 5432:5432 -d postgres:latest
# docker exec -it db psql -U devops -d contacts_db

# docker pull dpage/pgadmin4:latest
# docker run --name pgadmin_ui -e PGADMIN_DEFAULT_EMAIL=admin@gmail.com -e PGADMIN_DEFAULT_PASSWORD=admin -p 5050:80 -d dpage/pgadmin4

# openssl rand -hex 32 (create JWT_SECRET)
