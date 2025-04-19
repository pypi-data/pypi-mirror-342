# AppDog

[![ci](https://img.shields.io/github/actions/workflow/status/rodolphebarbanneau/appdog/ci.yml?branch=main&logo=github&label=ci)](https://github.com/rodolphebarbanneau/appdog/actions?query=event%3Apush+branch%3Amain+workflow%3Aci)
[![cov](https://codecov.io/gh/rodolphebarbanneau/appdog/branch/main/graph/badge.svg)](https://codecov.io/gh/rodolphebarbanneau/appdog)
[![pypi](https://img.shields.io/pypi/v/appdog.svg)](https://pypi.python.org/pypi/appdog)
[![versions](https://img.shields.io/pypi/pyversions/appdog.svg)](https://pypi.python.org/pypi/appdog)
[![downloads](https://static.pepy.tech/badge/appdog/month)](https://pepy.tech/project/appdog)
[![license](https://img.shields.io/github/license/rodolphebarbanneau/appdog.svg)](https://github.com/rodolphebarbanneau/appdog/blob/main/LICENSE)

Compose and generate effortlessly async API clients and MCP servers from any OpenAPI specifications.

<br>
<p align="center">
  <img src="https://raw.githubusercontent.com/rodolphebarbanneau/appdog/refs/heads/main/docs/appdog.gif" alt="AppDog demo">
</p>

## Overview

AppDog is a Python package that simplifies working with OpenAPI-based APIs by:

- Automatically generating fully typed Python clients from OpenAPI specifications
- Creating ready-to-use MCP (Model Context Protocol) servers for API integrations
- Managing multiple API clients in a single project with version locking
- Providing a simple CLI for adding, removing, managing API clients, and installing MCP servers

## Installation

```bash
uv add appdog
```

## Quick Start

### Initialize a project

```bash
# Create a new project in the current directory
appdog init

# Or specify a project directory
appdog init --project /path/to/project
```

### Add an API client

```bash
# Add a new API client from an OpenAPI spec URL or file
appdog add petstore --uri https://petstore3.swagger.io/api/v3/openapi.json
```

### List and show available APIs

```bash
# List all API clients in the project
appdog list

# Show details for a specific API client
appdog show petstore
```

### Upgrade API clients

```bash
# Sync API clients with the project registry
appdog sync --upgrade

# Lock API clients
appdog lock --upgrade
```

### Generate an MCP server

```bash
# Generate and install an MCP server with all registered APIs
appdog mcp install -n "My API Server"

# Or run the server directly
appdog mcp run -n "My API Server"

# Or run in development mode with inspector
appdog mcp dev -n "My API Server"
```

## Project Structure

After initializing a project and adding APIs, your project will have:

```
project/
├── apps.yaml     # Installed API appdog settings (auto-generated)
├── apps.lock     # Lock file with app specs and hashes (auto-generated)
└── ...           # Project files
```

## Using Generated Clients

After adding an API client, you can import and use it in your code:

```python
# Import generated client
import appdog.petstore

# Use the client
async def main() -> None:
    async with appdog.petstore.client as client:
        pets = await client.get_pet_find_by_status(status='available')
        print(pets)
```

And compose your own MCP server:

```python
import appdog.petstore
from fastmcp import FastMCP

mcp = FastMCP()

@mcp.tool()
async def hello_petstore() -> str:
    async with appdog.petstore.client as client:
        pets = await client.get_pet_find_by_status(status='available')
        return pets
```

## Environment Variables

API credentials can be configured using environment variables:

```
APPDOG_<CLIENT_NAME>_TOKEN=your_token
APPDOG_<CLIENT_NAME>_API_KEY=your_api_key
```

## MCP Integration

The package includes full support for MCP server generation:

1. Generate an MCP server file:
    ```bash
    appdog mcp install -n "My API Server"
    ```

2. Use with FastMCP or other MCP clients:
    ```python
    from appdog import Project
    from fastmcp import FastMCP
  
    mcp = FastMCP()

    project = Project.load(project_dir=PROJECT_DIR)
    project.mount(mcp)
    ```

## CLI Usage

### Global Options

- `--verbose`, `-v`: Enable verbose output
- `--debug`, `-d`: Enable all debug logs, including dependencies
- `--project`, `-p`: Specify project directory (defaults to current directory)

### Commands

#### Show CLI version

```bash
appdog version
```

#### Initialize Project

```bash
appdog init [--force] [--project PATH]
```

- `--force`: Force initialization even if config already exists

#### Add API Client

```bash
appdog add NAME --uri URI [--base-url URL] [OPTIONS]
```

- `NAME`: Application name
- `--uri`: OpenAPI specification URL or file path
- `--base-url`: Base URL for API calls
- `--include-methods`: Methods to include
- `--exclude-methods`: Methods to exclude
- `--include-tags`: Tags to include
- `--exclude-tags`: Tags to exclude
- `--force`: Overwrite application if it already exists with a different URI
- `--frozen`: Skip adding application specification in project lock file
- `--upgrade`: Force upgrading application specification
- `--sync`: Sync application specification with project registry

#### Remove API Client

```bash
appdog remove NAME [OPTIONS]
```

- `NAME`: Application name
- `--frozen`: Skip removing application specification from project lock file
- `--sync`: Sync application removal with project registry

#### List API Clients

```bash
appdog list [--project PATH]
```

#### Show API Client Details

```bash
appdog show NAME [--project PATH]
```

- `NAME`: Application name

#### Lock API Specifications

```bash
appdog lock [OPTIONS]
```

- `--force`: Overwrite application if it exists with a different URI
- `--upgrade`: Overwrite application specification with a different URI

#### Sync API Clients

```bash
appdog sync [OPTIONS]
```

- `--force`: Overwrite application if it exists with a different URI
- `--frozen`: Skip updating application specification in project lock file
- `--upgrade`: Force upgrading application specification

#### Generate MCP Server

```bash
appdog mcp [COMMAND] [OPTIONS]
```

Commands:
- `install`: Install applications in MCP client
- `run`: Run MCP applications in production mode
- `dev`: Run MCP applications in development mode with inspector

Each command supports specific options:

##### Common Options (all commands)
- `--name`, `-n`: Name of the MCP server (default: "AppDog MCP Server")
- `--force`: Overwrite server file if it exists
- `--project`, `-p`: Project directory (defaults to current)
- `--output`, `-o`: Output path for MCP server file

##### Install Command
```bash
appdog mcp install [OPTIONS]
```
- `--env-var`, `-v`: Environment variables in KEY=VALUE format
- `--env-file`, `-f`: Environment file with KEY=VALUE pairs
- `--with`: Additional packages to install in dev mode
- `--with-editable`, `-e`: Local packages to install in editable mode

##### Run Command
```bash
appdog mcp run [OPTIONS]
```
- `--transport`, `-t`: Transport to use for MCP run (stdio or sse)

##### Dev Command
```bash
appdog mcp dev [OPTIONS]
```
- `--with`: Additional packages to install in dev mode
- `--with-editable`, `-e`: Local packages to install in editable mode

## Advanced Usage

### Client Configuration

Create a custom `apps.yaml` to configure your API clients:

```yaml
petstore:
  uri: https://petstore3.swagger.io/api/v3/openapi.json
  base_url: https://petstore3.swagger.io/api/v3
  include_tags:
    - pet
    - store
```

### Custom Authentication

> For MCP usage, see [environment variables section](#environment-variables)

Create a client with custom authentication:

```python
from appdog.petstore import PetstoreClient

# Custom API key
client = PetstoreClient(api_key="YOUR_API_KEY")

# Custom headers
client = PetstoreClient(
    headers={"Authorization": "Bearer YOUR_TOKEN"}
)
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for information on contributing to the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
