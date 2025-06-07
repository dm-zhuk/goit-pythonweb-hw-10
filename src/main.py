from fastapi import FastAPI
from src.routers.contacts import router

app = FastAPI(title="Contacts API", description="Contacts management REST API")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")

# source .venv/bin/activate
# poetry run python src/main.py
# http://0.0.0.0:8000/docs


# curl -X POST http://localhost:8000/contacts/ -H "Content-Type: application/json" -d '{"first_name":"Kim","last_name":"Philby","email":"kimf@mail.co.uk","phone_number":"012223456789","birthday":"1985-05-06,"additional_data": "test-02"}'

# curl -X PUT http://localhost:8000/contacts/3 -H "Content-Type: application/json" -d '{"first_name":"Kim","last_name":"Philby","email":"kimf@mail.co.uk","phone_number":"01222","birthday":"1985-05-06","additional_data":"test-211(PUT)"}'

# python x_pycache.py
