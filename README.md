# TaskFlow

TaskFlow is a task management system built with FastAPI and Celery. It allows users to create, update, and manage tasks with different priorities and statuses.

## Features

- User authentication and authorization
- Task creation, update, and retrieval
- Task assignment and distribution based on priority and workload
- Background task processing with Celery
- Database interaction using SQLAlchemy

## Getting Started

### Prerequisites

- Python 3.10+
- Docker

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/SHASHA184/taskflow.git
    cd taskflow
    ```

2. Apply the database migrations:
    ```sh
    bash scripts/apply_migrations.sh
    ```

3. Load test data into the database:
    ```sh
    bash scripts/load_test_data.sh
    ```


### Running with Docker

1. Build and run the Docker containers:
    ```sh
    docker-compose up --build
    ```

## API Endpoints

### Authentication

- `POST /token`: Authenticate a user and return an access token.

### Users

- `GET /users/{id}`: Retrieve a user by ID.
- `GET /users/{id}/details`: Retrieve a user along with their tasks.
- `POST /users`: Create a new user.
- `PATCH /users/{id}`: Update a user.

### Tasks

- `POST /tasks`: Create a new task.
- `PATCH /tasks/{id}`: Update a task.
- `GET /tasks/`: Retrieve tasks assigned to the current user.
- `GET /tasks/count`: Count tasks by their status.
- `GET /tasks/{id}/details`: Retrieve detailed information about a task.