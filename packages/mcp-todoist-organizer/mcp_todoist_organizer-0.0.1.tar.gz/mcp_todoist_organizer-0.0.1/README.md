# Todoist MCP Server

A Model Context Protocol (MCP) server for Todoist integration. This server provides tools for interacting with Todoist, including managing tasks, projects, and tracking productivity.

## Features

- **Task Management**: Create, retrieve, update, and complete tasks
- **Project Management**: Create and retrieve projects
- **Label Management**: Retrieve labels for organization
- **Search**: Query for Todoist tasks using Todoist's filter syntax
- **Resources**: Access metadata about Todoist objects (tasks, projects, labels)
- **Prompts**: Templates for common Todoist workflows (task creation, project planning, productivity reports)

## Installation

```bash
pip install mcp-todoist-organizer
```

## Configuration

Set the following environment variable:

```bash
export TODOIST_API_TOKEN="your_api_token"
```

You can obtain a Todoist API token from the Todoist Integrations settings: [https://todoist.com/app/settings/integrations](https://todoist.com/app/settings/integrations)

## Usage

### Starting the server directly

```bash
mcp-todoist-organizer
```

### Using with UVX

```bash
uvx mcp-todoist-organizer
```

### Using with Claude Desktop

Add the following to your claude_desktop_config.json file:

```json
"mcp-todoist-organizer": {
  "command": "uvx",
  "args": [
    "mcp-todoist-organizer"
  ],
  "env": {
    "TODOIST_API_TOKEN": "your_api_token"
  }
}
```

Replace the environment variables with your actual Todoist credentials.

## Available Tools

* **get_tasks**: Get all active tasks
* **get_task**: Get details of a specific task
* **create_task**: Create a new task with optional project, due date, priority, and labels
* **complete_task**: Mark a task as complete
* **get_projects**: Get all projects
* **create_project**: Create a new project
* **get_labels**: Get all labels
* **search_tasks**: Search tasks using Todoist's filter syntax

## Available Resources

* **todoist://tasks**: List of all Todoist tasks
* **todoist://projects**: List of all Todoist projects
* **todoist://labels**: List of all Todoist labels

## Available Prompts

* **create_task**: Template for creating a new task
* **plan_project**: Template for planning a new project structure
* **productivity_report**: Template for generating a productivity report

## Version

0.0.1
