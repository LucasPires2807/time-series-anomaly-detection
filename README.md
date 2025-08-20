# Project Startup

This document provides instructions for setting up and running the project, both with and without Docker containers.

## Running with Docker

Follow these steps to run the application and the monitoring stack using Docker Compose.

### 1. Application

- **Build and start the main application container:**
   ```sh
   docker compose up --build -d
   ```

2. Monitoring with Prometheus and Grafana

The monitoring stack, defined in `docker-compose-monitoring.yml`, runs alongside the main application.

- Create the shared Docker network (only needs to be done once):

    ```sh
    docker network create monitoring-net
    ```

- Access `http://localhost:8000/docs` to see the API documentation.

- Start the monitoring services (Prometheus and Grafana) in detached mode:

    ```sh
    docker compose -f docker-compose-monitoring.yml up -d
    ```

- Access the services:

    - Prometheus: View metrics and targets at `http://localhost:9090`.

    - Grafana: Visualize data and build dashboards at `http://localhost:3000`.

        - Login: `admin`

        - Password: `admin`

## Running without container

### Install uv

- Mac/Linux:
    - Use curl to download the script and execute it with sh:
 
        `curl -LsSf https://astral.sh/uv/install.sh | sh`

    - If your system doesn't have curl, you can use wget:

        `wget -qO- https://astral.sh/uv/install.sh | sh`
    
    - Request a specific version by including it in the URL:

        `curl -LsSf https://astral.sh/uv/0.8.11/install.sh | sh`

- Windows:
    - Use irm to download the script and execute it with iex:

        `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

    Changing the execution policy allows running a script from the internet.

    - Request a specific version by including it in the URL:

        `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/0.8.11/install.p`


### Run the project

- Install the dependencies

`uv sync`

- Run the project

`uv run gunicorn -c gunicorn.conf.py`


### Sample training and prediction requests

**For training you can use:**

- series_id: `series_1`
- At the request body you can use
```
{
  "data": [
    { "timestamp": 0, "value": 0 },
    { "timestamp": 1, "value": 1 },
    { "timestamp": 2, "value": 2 },
    { "timestamp": 3, "value": 3 },
    { "timestamp": 4, "value": 4 },
    { "timestamp": 5, "value": 5 },
    { "timestamp": 6, "value": 6 },
    { "timestamp": 7, "value": 7 },
    { "timestamp": 8, "value": 8 },
    { "timestamp": 9, "value": 9 }
  ]
}
```

**For prediction you can use:**

- series_id: `series_1`
- version: `v1`
- At the request body you can use
```
{
  "timestamp": 0,
  "value": 0
}
```

**For plot you can use:**

- series_id: `series_1`
- version: `v1`

