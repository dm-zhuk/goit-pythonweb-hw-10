# Contacts Management REST API on Python v.3.13.2

The Contacts Management REST API is a web application designed to manage user contacts efficiently. Built with FastAPI, this API provides a robust and scalable solution for performing CRUD (Create, Read, Update, Delete) operations on user contact information.

## Features

- **User Authentication:** Implements a secure authentication mechanism to verify user identities.
- **JWT Authorization:** Utilizes JSON Web Tokens (JWT) for authorization, ensuring that all contact operations are performed only by registered users.
- **User-Specific Access:** Each user has access only to their own contacts, preventing unauthorized access to others' data.
- **Email Verification:** Supports email verification for newly registered users to confirm their identity.
- **Rate Limiting:** Limits the number of requests to the `/me` endpoint to enhance security and prevent abuse.
- **CORS Support:** Cross-Origin Resource Sharing is enabled, allowing secure interactions with the API from different origins.
- **User Avatar Updates:** Provides functionality for users to update their profile avatars, utilizing Cloudinary for image hosting.
- **Conflict Handling:** Returns HTTP 409 Conflict if a user tries to register with an existing email.
- **Password Security:** Hashes passwords before storing them in the database to ensure security.
- **Creation Responses:** Returns HTTP 201 Created status for successful user registrations and resource creation.
- **Authentication on POST Requests:** Requires user authentication for all POST requests, accepting user credentials (username and password) in the request body.
- **Unauthorized Access Handling:** Returns HTTP 401 Unauthorized if the user does not exist or if the password is incorrect.
- **Environment Variables:** All sensitive data is stored in a `.env` file, with no hard-coded secrets in the application code.
- **Docker Compose:** Uses Docker Compose to launch all services and databases, simplifying the deployment process.

## Technologies Used

- **FastAPI:** A modern, fast (high-performance) web framework for building APIs with Python 3.7+.
- **PostgreSQL:** A powerful, open-source relational database for storing user and contact information.
- **Redis:** Used for caching and rate limiting to enhance performance.
- **Cloudinary:** Service for hosting user avatars.
- **Docker:** Containerized application for easy deployment and scalability.

## Getting Started

To run this API locally, clone the repository and follow the instructions in the installation section:

# poetry install

# docker-compose up --build -d

# docker-compose exec web ls -l /app/src/services/templates

# openssl rand -hex 32 (create JWT_SECRET)

# Verify Redis is running:
- **docker exec -it redis-cache redis-cli ping**

## Project Structure
.
├── Dockerfile
├── README.md
├── docker-compose.yaml
├── img
├── poetry.lock
├── postgres_data/
├── pyproject.toml
└── src
    ├── main.py
    ├── __init__.py
    ├── database
    │   ├── __init__.py
    │   ├── connect.py
    │   └── models.py
    ├── repository
    │   ├── __init__.py
    │   ├── contacts.py
    │   └── users.py
    ├── routers
    │   ├── __init__.py
    │   ├── contacts.py
    │   ├── users.py
    │   └── utils.py
    ├── schemas
    │   ├── __init__.py
    │   └── schemas.py
    ├── services
    │   ├── auth.py
    │   ├── base.py
    │   ├── cloudinary_config.py
    │   ├── email.py
    │   ├── get_upload.py
    │   └── templates
    │       └── email_template.html
    ├── tests/
    └── utils.py
