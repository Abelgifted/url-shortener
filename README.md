# URL Shortener API

A production-inspired URL Shortener REST API built with **FastAPI**, **SQLite**, and **Python**. The application allows users to register accounts, create shortened URLs, redirect visitors to the original URLs, and track click statistics. The project follows clean software engineering principles, including modular design, database abstraction, Base62 URL encoding, proper error handling, and RESTful API development.

## Features

* User registration
* Create short URLs
* Redirect short URLs to their original destinations
* Track click counts
* Retrieve URL statistics
* SQLite database with indexed lookups
* Base62 short code generation
* Automatic database initialization
* Interactive API documentation with Swagger UI

## Project Structure

```text
url-shortener/
├── database.py        # Database operations




































































































├── models.py          # Base62 encoding/decoding
├── main.py            # FastAPI application
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

## API Endpoints

### Users

| Method | Endpoint              | Description         |
| ------ | --------------------- | ------------------- |
| POST   | `/api/users/register` | Register a new user |

### URLs

| Method | Endpoint                       | Description                  |
| ------ | ------------------------------ | ---------------------------- |
| POST   | `/api/urls`                    | Create a short URL           |
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

## Future Improvements

* User login and authentication (JWT)
* Password hashing with bcrypt
* Custom short URLs
* URL expiration
* QR code generation
* Rate limiting
* Redis caching
* Docker support
* Automated unit and integration tests
* Deployment to a cloud platform

## License

This project was built as a learning project to practice backend development, REST API design, database modeling, and software engineering principles using Python and FastAPI.
