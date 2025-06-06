from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(128), index=True)
    last_name = Column(String(128), index=True)
    email = Column(String(60), unique=True, index=True)
    phone_number = Column(String(15), unique=True, index=True)
    birthday = Column(Date)
    additional_data = Column(String, nullable=True)
