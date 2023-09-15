# Connect Application API

This application is built using Flask, a Python web framework. It provides functionality for user authentication, event management, and file handling.

## Table of Contents
- [Getting Started](#getting-started)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Database Models](#database-models)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

These instructions will help you set up and run the backend application on your local machine.

### Features

- User registration and authentication
- Event creation, retrieval, updating, and deletion
- File uploads for events
- User-specific event management

### Prerequisites

Before you begin, ensure you have the following installed on your machine:

- Python (version 3.7 or higher)
- pip (Python package manager)

### Installation

1. Clone this repository to your local machine:

   ```shell
   git clone <repository-url>

2. Change to the project directory:
   ```shell
   cd <project-directory>

3. Activate the virtual environment:
   - On Windows:
      ```shell
      venv\Scripts\activate
   - On macOS and Linux:
     ```shell
     source venv/bin/activate

4. Install the required packages:
   ```shell
     pip install -r requirements.txt

### Configuration
Before running the application, make sure to set up your environment variables. You can do this by creating a .env file in the project directory and adding the following variables:

- SECRET_KEY: A secret key for Flask's session management.
- SQLALCHEMY_DATABASE_URI: The URI for your PostgreSQL database.
- SQLALCHEMY_TEST_DATABASE_URI: The URI for your test database (if applicable).

By default, the application will run on http://localhost:5000.

### API Endpoints
Here are the available API endpoints:

### Users
- POST /users/register: Register a new user.
- POST /users/login: Log in with a registered user.
- POST /users/logout: Log out a logged-in user.
- GET /users/<username>: Retrieve user information.
- GET /users: Retrieve information for all users.
- PUT /users/<user_id>: Update user information.
- DELETE /users/<user_id>: Delete a user.

### Events
- POST /events/create_event: Create a new event.
- GET /events/<event_id>: Retrieve information for a specific event.
- GET /events: Retrieve information for all events.
- GET /events/all: Retrieve information for all events (alternative endpoint).
- PUT /events/<event_id>: Update event information.
- DELETE /events/<event_id>: Delete an event.

### User Events
- GET /users/<user_id>/events: Retrieve all events for a specific user.

### Database Models
The application uses SQLAlchemy to interact with the database. Here are the relevant database models:

- `User`: Represents a user with username, email, and password fields.
- `Event`: Represents an event with title, event type, location, date, description, and file data fields.
