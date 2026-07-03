# URL Shortener API

A production-inspired URL Shortener REST API built with **FastAPI**, **SQLite**, and **Python**. The application allows users to register accounts, create shortened URLs, redirect visitors to the original URLs, and track click statistics. The project follows clean software engineering principles, including modular design, database abstraction, Base62 URL encoding, proper error handling, and RESTful API development.

## Features

* User registration and authentication (JWT)
* Secure password hashing with bcrypt
* Create short URLs (authenticated and anonymous)
* Redirect short URLs to their original destinations
* Track click counts and view statistics
* User-specific URL management
* SQLite database with indexed lookups
* Base62 short code generation
* Automatic database initialization
* Interactive API documentation with Swagger UI
* Comprehensive test coverage

## Project Structure

```text
url-shortener/
├── main.py            # FastAPI application and routes
├── database.py        # Database operations and schema
├── models.py          # Base62 encoding/decoding
├── auth.py            # Authentication and JWT tokens
├── test_auth.py       # Authentication tests
├── test_database.py   # Database tests
├── requirements.txt
├── .gitignore
└── README.md
```

## Technologies Used

* Python 3
* FastAPI
* SQLite
* Uvicorn
* Pydantic

## Installation

1. Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/url-shortener.git
cd url-shortener
```

2. Create and activate a virtual environment:

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the API server:

```bash
python main.py
```

The server will run at:

```
http://localhost:8000
```

Interactive API documentation is available at:

```
http://localhost:8000/docs
```

Alternative OpenAPI documentation:

```
http://localhost:8000/redoc
```

## Live Demo

**API Base URL:**
```
https://url-shortener-1xuu.onrender.com
```

**Swagger Documentation:**
```
https://url-shortener-1xuu.onrender.com/docs
```

## API Endpoints

### General

| Method | Endpoint | Description                              |
| ------ | -------- | ---------------------------------------- |
| GET    | `/`      | API health check and service information |

### Users

| Method | Endpoint              | Description       |
| ------ | --------------------- | ----------------- |
| POST   | `/api/users/register` | Register a new user |
| POST   | `/api/users/login`    | Login and get JWT token |

### URLs

| Method | Endpoint                       | Description                  |
| ------ | ------------------------------ | ---------------------------- |
| POST   | `/api/urls`                    | Create a short URL           |
| GET    | `/api/urls`                    | List user's shortened URLs (authenticated) |
| GET    | `/api/urls/{short_code}/stats` | View URL statistics          |
| GET    | `/{short_code}`                | Redirect to the original URL |

## Database Schema

The application uses two tables:

* **users**
* **urls**

Each URL stores:

* Short code
* Original URL
* Click count
* Creation timestamp
* Optional expiration date
* Associated user (optional)

## Example Response

```json
{
    "short_code": "00000g",
    "long_url": "https://www.google.com",
    "short_url": "http://localhost:8000/00000g",
    "click_count": 0
}
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Protected endpoints require a valid token in the `Authorization: Bearer <token>` header.

### Getting a Token

1. Register a user: `POST /api/users/register`
2. Login with credentials: `POST /api/users/login`
3. Use the returned `access_token` for authenticated requests

## Future Improvements

* Custom short URLs
* URL expiration enforcement
* QR code generation
* Rate limiting
* Redis caching
* Docker support
* Comprehensive integration tests
* Deployment to a cloud platform
* Admin dashboard
* Analytics and reporting

## License

This project was built as a learning project to practice backend development, REST API design, database modeling, and software engineering principles using Python and FastAPI.
