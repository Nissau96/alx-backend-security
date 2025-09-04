# alx-backend-security
A robust Django IP tracking system for security &amp; analytics. 🔐 This project uses middleware to implement logging, blacklisting, geolocation, and rate limiting. Built with best practices for performance, privacy (GDPR/CCPA), and compliance to protect your application and understand user behavior.

## Project Overview

In modern web applications, tracking IP addresses is critical for:
- **Security**: Identifying and blocking malicious actors, bots, and scrapers.
- **Analytics**: Understanding user geography and traffic patterns.
- **Compliance**: Adhering to legal requirements for data logging and privacy.

This repository demonstrates how to build these features from the ground up, focusing on performance, scalability, and ethical considerations.

## Features

| Status | Feature                | Description                                                                 |
| :----: | ---------------------- | --------------------------------------------------------------------------- |
|   ✅    | **IP Logging** | Middleware to log the IP, timestamp, and path of every request.             |
|   ✅    | **IP Blacklisting** | Block requests from known malicious IP addresses via middleware.                           |
|   🔲    | **Geolocation** | Map IP addresses to geographic locations (country, city, etc.).             |
|   | **Rate Limiting** | Prevent brute-force attacks and service abuse.                              |
|   | **Anomaly Detection** | Identify suspicious traffic patterns using statistical methods.             |
|   | **Privacy & Compliance** | Tools for IP anonymization and data retention policies (GDPR/CCPA).         |


## Tech Stack

- **Framework**: Django
- **Libraries**:
  - `django-ipware`: For reliable client IP address retrieval.
  - `celery`: For running intensive tasks asynchronously.
  - `django-ratelimit`: For easy implementation of rate limiting.
  - `redis`: For high-performance caching and lookups (blacklisting, rate limiting).
  - `geoip2`: For IP geolocation services.
  - `scikit-learn`: For machine learning-based anomaly detection.

## Getting Started

### Prerequisites

- Python 3.8+
- Django 4.x
- Git

### Installation and Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Nissau96/alx-backend-security.git](https://github.com/Nissau96/alx-backend-security.git)
    cd alx-backend-security
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    *(Create a `requirements.txt` file and add `Django` and `django-ipware` to start)*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000/`.

---

## Implemented Tasks

### Task 0: Basic IP Logging Middleware

-   **Objective**: Log the IP address, timestamp, and path of every incoming request.
-   **Implementation**:
    -   A `RequestLog` model was created in `ip_tracking/models.py` to store request data.
    -   `IPLoggingMiddleware` was implemented in `ip_tracking/middleware.py` to intercept requests, get the client IP using `django-ipware`, and save a `RequestLog` instance to the database.
    -   The middleware and app were registered in `settings.py` to activate the system.

### Task 1: IP Blacklisting
- **Objective**: Block requests from a predefined list of IP addresses.
- **Implementation**:
    - A `BlockedIP` model was added to `ip_tracking/models.py` to store banned IPs.
    - The `IPLoggingMiddleware` was updated to check the incoming request's IP against the `BlockedIP` table. If the IP is found, it returns an `HttpResponseForbidden` (403).
    - A custom management command, `block_ip`, was created. It allows adding an IP to the blacklist from the terminal (e.g., `python manage.py block_ip 123.45.67.89 --reason "Spam activity"`).
