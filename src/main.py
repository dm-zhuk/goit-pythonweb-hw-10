# src/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.database.connect import get_db
from src.routers.contacts import router


app = FastAPI(title="Contacts API", description="Contacts management REST API")
app.include_router(router)


@app.get("/", name="Root Endpoint")
def read_root():
    return {"message": "Welcome to the Contacts API v2.0"}


@app.get("/api/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database not reachable",
            )
        return {"message": "Database is reachable!"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        print(result)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database is not configured correctly",
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error connecting to the database",
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

# source .venv/bin/activate
# fastapi dev src/main.py
# http://localhost:5050/login?next=/
# http://0.0.0.0:8000/docs


# curl -X POST http://localhost:8000/contacts/ -H "Content-Type: application/json" -d '{"first_name":"Kim","last_name":"Philby","email":"kimf@mail.co.uk","phone_number":"012223456789","birthday":"1985-05-06,"additional_data": "test-02"}'

# curl -X PUT http://localhost:8000/contacts/3 -H "Content-Type: application/json" -d '{"first_name":"Kim","last_name":"Philby","email":"kimf@mail.co.uk","phone_number":"01222","birthday":"1985-05-06","additional_data":"test-211(PUT)"}'

# python x_pycache.py


# docker run --name db -e POSTGRES_USER=devops -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=contacts_db -p 5432:5432 -d postgres:latest
# docker exec -it db psql -U devops -d contacts_db

# docker pull dpage/pgadmin4:latest
# docker run --name pgadmin_ui -e PGADMIN_DEFAULT_EMAIL=admin@gmail.com -e PGADMIN_DEFAULT_PASSWORD=admin -p 5050:80 -d dpage/pgadmin4

# openssl rand -hex 32 (create JWT_SECRET)
