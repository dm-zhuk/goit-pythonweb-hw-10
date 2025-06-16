from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from src.database.connect import init_db
from src.services.base import settings
from src.routers import contacts, users, utils
from src.services.redis import get_r_client

app = FastAPI(title="Contacts API", description="Contacts management REST API")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.BASE_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Rate limiting and Redis init/close
@app.on_event("startup")
async def startup():
    await FastAPILimiter.init(get_r_client())
    await init_db()


@app.on_event("shutdown")
async def shutdown():
    await get_r_client().close()


app.include_router(utils.router, prefix="/api")
app.include_router(contacts.router, prefix="/api/contacts")
app.include_router(users.router)

# source .venv/bin/activate
# clear cache —force
# docker-compose down
# docker-compose up --build -d

# docker-compose exec web ls -l /app/src/services/templates

# python del_pycache.py

# openssl rand -hex 32 (create JWT_SECRET)
