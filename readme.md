# URL Shortener

A simple URL shortener built using Flask and SQLAlchemy.

## Overview

This project is a basic URL shortener implemented in Python using the Flask web framework and SQLAlchemy for database management. It allows users to shorten long URLs into unique, easy-to-share short codes.

## Getting Started

### Prerequisites

Before running the application, make sure you have the following installed:

- Python 3.x
- Flask
- SQLAlchemy

You can install the required dependencies using the following command:

```bash
pip install Flask SQLAlchemy
```

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/shameemm/URL-Shortner-Flask/.git
    pip install -r requirements.txt
    ```

2. **Run the application:**

    ```bash
    python app.py
    ```

    The application will be accessible at `http://localhost:5000`.

### Usage

- To shorten a URL, send a POST request to `http://localhost:5000/shorten` with the `long_url` parameter.
- To access the original URL, use the generated short URL: `http://localhost:5000/{short_code}`.
- Retrieve URL metadata at `http://localhost:5000/metadata/{short_code}`.

## Endpoints

- **POST /shorten**: Shorten a long URL.
  - Parameters:
    - `long_url` (string): The long URL to be shortened.
  - Example:

    ```bash
    curl -X POST -d "long_url=https://www.example.com" http://localhost:5000/shorten
    ```

- **GET /{short_code}**: Redirect to the original URL.
  - Example:

    ```bash
    curl http://localhost:5000/{short_code}
    ```

- **GET /metadata/{short_code}**: Retrieve metadata for a short URL.
  - Example:

    ```bash
    curl http://localhost:5000/metadata/{short_code}
    ```

