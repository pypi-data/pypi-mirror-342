# Cyberwave Backend: Robot Registry Service

**Version:** 1.0.0

This document provides an overview of the backend architecture for the Robot Registry Service microservice, part of the Cyberwave platform.

## Table of Contents

1.  [Overview & Purpose](#overview--purpose)
2.  [Architectural Principles](#architectural-principles)
3.  [Technology Stack](#technology-stack)
4.  [Directory Structure](#directory-structure)
5.  [Architectural Layers Explained](#architectural-layers-explained)
    *   [API Layer (`src/api/`)](#api-layer-srcapi)
    *   [Service Layer (`src/services/`)](#service-layer-srcservices)
    *   [Repository Layer (`src/repository/`)](#repository-layer-srcrepository)
    *   [Models Layer (`src/models/`)](#models-layer-srcmodels)
    *   [Schemas Layer (`src/schemas/`)](#schemas-layer-srcschemas)
    *   [Database Layer (`src/db/`)](#database-layer-srcdb)
    *   [Core Layer (`src/core/`)](#core-layer-srccore)
    *   [Main Application (`src/main.py`)](#main-application-srcmainpy)
6.  [Data Flow Example](#data-flow-example)
7.  [Database Migrations](#database-migrations)
8.  [Testing Strategy](#testing-strategy)
9.  [Configuration](#configuration)
10. [Local Development Setup](#local-development-setup)
11. [Deployment](#deployment)

---

## 1. Overview & Purpose

The Robot Registry Service service is responsible for managing the registration, metadata, and relationships of Workspaces, Projects, Levels, Robots, and Fixed Assets within the Cyberwave system. It provides a RESTful API for creating, reading, updating, and deleting these core entities.

This service interacts with potentially publishing events to a Message Bus upon entity changes, or being called by the Mission Orchestrator.

---

## 2. Architectural Principles

The architecture is designed based on the following principles:

*   **Separation of Concerns:** Clear distinction between API handling, business logic, data access, and data definition.
*   **Layered Architecture:** Code is organized into distinct layers (API, Service, Repository, Model) with well-defined responsibilities.
*   **Dependency Injection:** FastAPI's DI is heavily utilized for decoupling components (especially database sessions and dependencies between layers) and enhancing testability.
*   **Explicit Data Contracts:** Pydantic schemas define all data structures used for API input validation and output serialization.
*   **Repository Pattern:** Abstracts data persistence logic, decoupling business logic from specific database interactions.
*   **Asynchronous Operations:** Leverages Python's `asyncio` and FastAPI's async capabilities for non-blocking I/O (e.g., async database operations).
*   **Type Hinting:** Extensive use of Python type hints for improved code clarity, static analysis, and developer tooling.
*   **Testability:** Structured to facilitate comprehensive unit, integration, and potentially end-to-end testing.

---

## 3. Technology Stack

*   **Framework:** FastAPI
*   **Language:** Python ^3.10 (Requires **Python 3.11+** for development due to dependencies/environment setup)
*   **Database:** SQLite (default for local dev via `aiosqlite`), PostgreSQL support intended for production.
*   **ORM:** SQLAlchemy (with AsyncSession)
*   **Migrations:** Alembic
*   **Data Validation/Serialization:** Pydantic
*   **Dependency Management:** Poetry
*   **Testing:** Pytest, HTTPX (for async test client)
*   **Containerization:** Docker (Configuration TBD)
*   **CI/CD:** GitHub Actions (TBD)
*   **Infrastructure:** Kubernetes, Cloud Provider Services (TBD)

---

## 4. Directory Structure

```plaintext
cyberwave-backend/
├── alembic/                 # Alembic migrations
│   └── versions/            # Generated migration scripts
│   ├── env.py               # Alembic environment setup
│   └── script.py.mako       # Migration script template
├── scripts/                 # Utility scripts
│   └── seed_db.py           # Script to load initial data
├── src/                     # Main source code
│   ├── api/                 # API Layer
│   │   └── v1/              # API Version 1
│   │       ├── endpoints/   # Resource-specific routers (workspaces.py, robots.py, ...)
│   │       │   └── __init__.py
│   │       ├── __init__.py
│   │       └── router.py    # Aggregate v1 router
│   ├── core/                # Core config, exceptions, etc.
│   │   ├── __init__.py
│   │   └── config.py        # Pydantic settings
│   ├── db/                  # Database setup
│   │   ├── __init__.py
│   │   ├── base_class.py    # SQLAlchemy Base
│   │   └── session.py       # Async engine and session factory
│   ├── models/              # SQLAlchemy ORM Models (user.py, workspace.py, ...)
│   │   └── __init__.py
│   ├── repository/          # Data Access Layer (base.py, user.py, workspace.py, ...)
│   │   └── __init__.py
│   ├── schemas/             # Pydantic Schemas (base.py, user.py, workspace.py, ...)
│   │   └── __init__.py
│   ├── services/            # Business Logic Layer (workspace_service.py, robot_service.py, ...)
│   │   └── __init__.py
│   ├── __init__.py
│   └── main.py              # FastAPI App Entrypoint
├── tests/                   # Automated tests
│   ├── api/
│   │   └── v1/              # API v1 tests (test_workspaces.py, test_robots.py, ...)
│   │       └── __init__.py
│   └── __init__.py
├── .env.example             # Environment variable template
├── .gitignore
├── alembic.ini              # Alembic configuration
├── cyberwave.db             # SQLite database file (local dev)
├── pyproject.toml           # Poetry dependencies and project config
├── README.md                # This file
└── seed-data.json           # Initial data for seeding
```
---

## 5. Architectural Layers Explained

### API Layer (`src/api/`)

*   **Responsibility:** Handles incoming HTTP requests, validates input data using Pydantic schemas, invokes appropriate business logic via the Service Layer, formats responses using Pydantic schemas, and handles HTTP-specific exceptions.
*   **Components:** FastAPI `APIRouter`s grouped by resource/feature under versioned directories (e.g., `v1/endpoints/`). Common dependencies (like `get_db_session`) are defined in `deps.py`.

### Service Layer (`src/services/`)

*   **Responsibility:** Contains the core business logic of the application. Orchestrates operations, enforces business rules, coordinates calls to repositories, and potentially dispatches events or interacts with other services.
*   **Components:** Service classes or functions (e.g., `RobotService`). Takes dependencies (like Repositories) via constructor or function arguments (using DI). Should be independent of HTTP concerns.

### Repository Layer (`src/repository/`)

*   **Responsibility:** Abstracts data persistence operations. Provides an interface (e.g., `RobotRepository`) with methods like `get_by_id`, `list_by_project`, `create`, `update`. Handles interactions with SQLAlchemy ORM models and the database session.
*   **Components:** Repository classes implementing data access logic for specific models. Takes an `AsyncSession` as a dependency.

### Models Layer (`src/models/`)

*   **Responsibility:** Defines the database table structures using SQLAlchemy's declarative ORM models. Includes column definitions, data types, constraints, and relationships between tables.
*   **Components:** Python classes inheriting from a declarative base (`db/base_class.py`).

### Schemas Layer (`src/schemas/`)

*   **Responsibility:** Defines the data shapes (contracts) for API requests and responses using Pydantic models. Used for automatic data validation, serialization, and generating OpenAPI documentation.
*   **Components:** Pydantic `BaseModel` classes (e.g., `RobotCreate`, `RobotUpdate`, `RobotInDB`). Separated from ORM Models.

### Database Layer (`src/db/`)

*   **Responsibility:** Manages database connection setup (engine), session creation (`AsyncSessionLocal`), and potentially provides the declarative base class for ORM models.
*   **Components:** `session.py` (engine, session factory), `base_class.py` (DeclarativeBase).

### Core Layer (`src/core/`)

*   **Responsibility:** Holds application-wide configurations (`config.py`), custom exceptions (`exceptions.py`), security utilities (`security.py`), and potentially other core functionalities not specific to a single business domain.

### Main Application (`src/main.py`)

*   **Responsibility:** Instantiates the FastAPI application, includes API routers, configures middleware (e.g., CORS), sets up global exception handlers, and defines application startup/shutdown events.

---

## 6. Data Flow Example (e.g., Creating a Robot)

1.  **HTTP Request:** `POST /api/v1/robots/` with JSON payload arrives at the API Gateway and is routed to this service.
2.  **API Layer (`api/v1/endpoints/robots.py`):**
    *   The corresponding path operation function is invoked.
    *   FastAPI validates the incoming JSON payload against the `schemas.RobotCreate` Pydantic model.
    *   Dependencies are resolved (e.g., `get_db_session`, `get_current_user`).
    *   The API handler calls the appropriate method in the `services.RobotService` (e.g., `robot_service.create_robot(robot_data=...)`).
3.  **Service Layer (`services/robot_service.py`):**
    *   The `create_robot` method receives the validated data (as a `schemas.RobotCreate` object).
    *   It performs business logic (e.g., checks if the associated Level exists by calling `LevelRepository`, generates a unique internal ID if needed).
    *   It calls the `repository.RobotRepository.create()` method, passing the necessary data (often converting the schema object to dictionary or directly using its attributes).
    *   It might perform post-creation actions (e.g., dispatch an event to the message bus: `messaging.publish_event("robot_created", ...)`).
    *   It returns the newly created robot data (likely as a `schemas.Robot` object).
4.  **Repository Layer (`repository/robot_repository.py`):**
    *   The `create()` method receives data.
    *   It creates an instance of the `models.Robot` ORM model.
    *   It uses the injected `AsyncSession` to add the new model instance (`db.add(db_robot)`).
    *   It typically calls `await db.commit()` and `await db.refresh(db_robot)` (though transaction handling might be managed higher up, e.g., in a service decorator or middleware, using Unit of Work pattern).
    *   It returns the persisted `models.Robot` object.
5.  **Service Layer:** Receives the ORM model, potentially converts it back to a Pydantic schema for return.
6.  **API Layer:** Receives the result from the service, formats the final HTTP response (using the `response_model` Pydantic schema), and sends it back to the client.

---

## 7. Database Migrations

Database schema changes are managed using **Alembic**.

*   **Configuration:** `alembic.ini` and `alembic/env.py`.
*   **Generate Migration:** `alembic revision --autogenerate -m "Description of changes"`
*   **Apply Migration:** `alembic upgrade head`
*   **Downgrade Migration:** `alembic downgrade -1`

**Never modify the database schema directly or rely on `create_all()` in staging/production.**

---

## 8. Testing Strategy

*   **Framework:** Pytest
*   **End-to-End (E2E) Tests:** For local development verification, E2E tests (`tests/api/`) are run against the live development server using `httpx.AsyncClient`. These tests assume a migrated and seeded database (`cyberwave.db`).
*   **Running E2E Tests:**
    *   **Automated Script (Recommended):**
        *   Make the script executable: `chmod +x run_e2e_tests.sh`
        *   Run the script: `./run_e2e_tests.sh`
        *   This script automatically activates the virtual environment, starts the server, waits for it to be ready, runs `pytest`, stops the server, and reports results.
        *   You can pass arguments to pytest, e.g.: `./run_e2e_tests.sh -k "frictionless" -v`
    *   **Manual:** Activate the virtual environment (`source ../.venv/bin/activate`), start the server (`../.venv/bin/python -m uvicorn ...`) in one terminal, and run `pytest` (or `../.venv/bin/pytest`) in another terminal.
*   **Unit Tests:** (Future) Test individual functions/methods in isolation (especially in services, repositories, core utilities). Mock dependencies (like database sessions or repositories).
*   **Integration Tests:** (Future) Test the interaction between layers, typically starting from the API layer using FastAPI's `TestClient`. Often use a dedicated test database.
*   **Fixtures (`conftest.py`):** (Future) Used extensively to provide reusable test setup (e.g., test client instance, test database session overrides, creating mock data).
*   **Factories:** (Future) Use libraries like `factory_boy` to generate realistic test data easily.
*   **Coverage:** (Future) Aim for high test coverage, monitored via tools like `pytest-cov`.

---

## 9. Configuration

*   Configuration is managed via environment variables, loaded into a Pydantic `Settings` class (`src/core/config.py`).
*   An `.env` file can be used for local development (ensure it's in `.gitignore`).
*   An `.env.example` file shows required environment variables.

---

## 10. Local Development Setup

1.  **Prerequisites:** Python **3.11+**, Poetry.
2.  **Clone:** `git clone [repository-url]` and `cd cyberwave-backend`
3.  **Create & Activate Virtual Environment:**
    *   Go to the parent directory: `cd ..`
    *   Ensure you have Python 3.11+ available (e.g., via `brew install python@3.11`). Find its path using `which python3.11`.
    *   Create the venv using the **full path** to your Python 3.11+ executable: `/path/to/your/python3.11 -m venv .venv`
    *   Activate it: `source .venv/bin/activate` (Verify with `python --version`)
    *   Navigate back: `cd cyberwave-backend`
4.  **Install Dependencies:** Install Poetry if needed (`pip install poetry`) and then run `poetry install`.
5.  **Environment:** Copy `.env.example` to `.env`. The default `DATABASE_URL` points to the local SQLite file.
6.  **Run Migrations:** Apply database migrations to create the schema in `cyberwave.db`: `../.venv/bin/alembic upgrade head`
7.  **Seed Database (Optional):** Populate the database with initial data: `../.venv/bin/python scripts/seed_db.py`
8.  **Run Server:** Start the FastAPI server: `../.venv/bin/python -m uvicorn src.main:app --host 0.0.0.0 --port 8000` (Use `python -m uvicorn` or the direct path if `uvicorn` command is not found).
9.  **Access Docs:** `http://localhost:8000/docs`
10. **Run Tests:** In a **separate terminal** (with the server running), activate the venv (`source ../.venv/bin/activate` from `cyberwave-backend`) and run the tests: `../.venv/bin/pytest`.

---

## 11. Deployment

*   The application is containerized using the provided `Dockerfile`.
*   Deployment is typically managed via Kubernetes using Helm charts or similar orchestration tools.
*   CI/CD pipelines automate testing, building the Docker image, and deploying to different environments (dev, staging, prod).
*   Ensure proper configuration (environment variables, secrets) is injected into the deployment environment.

--- 