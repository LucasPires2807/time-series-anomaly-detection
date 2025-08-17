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
