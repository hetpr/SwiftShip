# SwiftShip

SwiftShip is a Flask-based web service application that demonstrates the use of microservices and Service-Oriented Architecture (SOA) principles.
It provides optimized route calculations and estimated delivery times through independent Flask services communicating via REST APIs.

## Overview

Instead of a single monolithic app, SwiftShip is composed of three microservices:

- Frontend Service – Main Flask app that handles user interaction
- Route Service – Calculates optimized delivery routes using Dijkstra’s Algorithm
- ETA Service – Estimates delivery time based on distance and conditions

Each service runs independently and communicates through HTTP requests, ensuring modularity and scalability.

## Tech Stack

- Language: Python 3.10+
- Framework: Flask
- Database: SQLite
- Frontend: HTML, CSS, Bootstrap, Jinja2
- API Communication: REST (via `requests`)
- Environment Management: python-dotenv

## Installation

1. Clone the repository

    git clone https://github.com/<your-username>/SwiftShip.git
    cd SwiftShip

2. Create a virtual environment

    python -m venv venv

    # macOS / Linux
    source venv/bin/activate

    # Windows (PowerShell)
    # .\venv\Scripts\Activate.ps1

    # Windows (cmd)
    # venv\Scripts\activate

3. Install dependencies

    pip install -r requirements.txt

4. Run each Flask service (open three terminals)

    # Terminal 1
    cd eta_service
    python app.py

    # Terminal 2
    cd ../route_service
    python app.py

    # Terminal 3
    cd ../frontend_service
    python app.py

5. Open the app in your browser:

    http://localhost:5000

## Features

- Modular Flask microservices architecture
- RESTful API communication between services
- Route optimization using Dijkstra’s Algorithm
- ETA prediction based on route and distance
- Lightweight, easy to extend, and maintainable

## Future Improvements

- Integrate real-time route data using Google Maps or OpenStreetMap
- Add authentication and user profiles
- Dockerize and deploy to cloud (AWS, Render, etc.)
- Replace rule-based ETA with ML-based prediction

## Contributors

- Het Prajapati (22BCP039)
- Riddhi Shah (22BCP098)
- Guided by Dr. Punit Gupta, PDEU

A simple and scalable example of Flask microservices working together — built for learning and demonstration.
