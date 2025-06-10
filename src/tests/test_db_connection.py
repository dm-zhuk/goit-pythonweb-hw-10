from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://devops:admin@localhost:5432/contacts_db"
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print(result.fetchone())
except Exception as e:
    print(f"Error: {e}")
