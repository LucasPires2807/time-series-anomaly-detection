# Project startup

## Install uv

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


## Running without container

- Install the dependencies

`uv sync`

- Run the project

`uv run gunicorn -c gunicorn.conf.py`
