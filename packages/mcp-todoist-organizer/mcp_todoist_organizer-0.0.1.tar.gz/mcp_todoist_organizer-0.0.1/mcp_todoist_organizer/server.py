# server.py
import sys
import os
import json
from typing import Dict, List, Optional, Any, Union
import httpx
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Todoist MCP")

# Environment variables for Todoist configuration
TODOIST_API_TOKEN = os.environ.get("TODOIST_API_TOKEN")

# Todoist API base URL
TODOIST_API_BASE = "https://api.todoist.com/rest/v2"

# Check if environment variables are set
if not TODOIST_API_TOKEN:
    print("Warning: Todoist environment variables not fully configured. Set TODOIST_API_TOKEN.", file=sys.stderr)

# Helper function for API requests
async def make_todoist_request(method: str, endpoint: str, data: Dict = None) -> Dict:
    """
    Make a request to the Todoist API.
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint (without base URL)
        data: Data to send (for POST/PUT)
    
    Returns:
        Response from Todoist API as dictionary
    """
    url = f"{TODOIST_API_BASE}{endpoint}"
    headers = {
        "Authorization": f"Bearer {TODOIST_API_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        if method.upper() == "GET":
            response = await client.get(url, headers=headers)
        elif method.upper() == "POST":
            response = await client.post(url, headers=headers, json=data)
        elif method.upper() == "PUT":
            response = await client.put(url, headers=headers, json=data)
        elif method.upper() == "DELETE":
            response = await client.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        if response.status_code >= 400:
            return {
                "error": True,
                "status_code": response.status_code,
                "message": response.text
            }
        
        if response.status_code == 204:  # No content
            return {"success": True}
            
        return response.json()

# === TOOLS ===

@mcp.tool()
async def get_tasks() -> str:
    """
    Get all active tasks.
    """
    result = await make_todoist_request("GET", "/tasks")
    
    if "error" in result:
        return f"Error retrieving tasks: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def get_task(task_id: str) -> str:
    """
    Get details of a specific task.
    
    Args:
        task_id: The Todoist task ID
    """
    result = await make_todoist_request("GET", f"/tasks/{task_id}")
    
    if "error" in result:
        return f"Error retrieving task: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def create_task(content: str, 
                     project_id: Optional[str] = None, 
                     due_string: Optional[str] = None, 
                     priority: Optional[int] = None, 
                     label_ids: Optional[List[str]] = None) -> str:
    """
    Create a new task in Todoist.
    
    Args:
        content: Task content/description
        project_id: ID of the project (optional)
        due_string: Due date in natural language (optional)
        priority: Task priority (1-4, 4 is highest) (optional)
        label_ids: List of label IDs (optional)
    """
    data = {"content": content}
    
    if project_id:
        data["project_id"] = project_id
    if due_string:
        data["due_string"] = due_string
    if priority:
        data["priority"] = priority
    if label_ids:
        data["label_ids"] = label_ids
    
    result = await make_todoist_request("POST", "/tasks", data)
    
    if "error" in result:
        return f"Error creating task: {result.get('message', 'Unknown error')}"
    
    return f"Task created successfully: {json.dumps(result, indent=2)}"

@mcp.tool()
async def complete_task(task_id: str) -> str:
    """
    Mark a task as complete.
    
    Args:
        task_id: The Todoist task ID
    """
    result = await make_todoist_request("POST", f"/tasks/{task_id}/close")
    
    if "error" in result:
        return f"Error completing task: {result.get('message', 'Unknown error')}"
    
    return "Task completed successfully"

@mcp.tool()
async def get_projects() -> str:
    """
    Get all projects.
    """
    result = await make_todoist_request("GET", "/projects")
    
    if "error" in result:
        return f"Error retrieving projects: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def create_project(name: str, color: Optional[str] = None) -> str:
    """
    Create a new project in Todoist.
    
    Args:
        name: Project name
        color: Project color (optional)
    """
    data = {"name": name}
    
    if color:
        data["color"] = color
    
    result = await make_todoist_request("POST", "/projects", data)
    
    if "error" in result:
        return f"Error creating project: {result.get('message', 'Unknown error')}"
    
    return f"Project created successfully: {json.dumps(result, indent=2)}"

@mcp.tool()
async def get_labels() -> str:
    """
    Get all labels.
    """
    result = await make_todoist_request("GET", "/labels")
    
    if "error" in result:
        return f"Error retrieving labels: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.tool()
async def search_tasks(query: str) -> str:
    """
    Search tasks using Todoist's filters.
    
    Args:
        query: Search query using Todoist's filter syntax
    """
    result = await make_todoist_request("GET", f"/tasks?filter={query}")
    
    if "error" in result:
        return f"Error searching tasks: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

# === RESOURCES ===

@mcp.resource("todoist://tasks")
async def get_tasks_resource() -> str:
    """Get a list of all Todoist tasks."""
    result = await make_todoist_request("GET", "/tasks")
    
    if "error" in result:
        return f"Error retrieving tasks: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.resource("todoist://projects")
async def get_projects_resource() -> str:
    """Get a list of all Todoist projects."""
    result = await make_todoist_request("GET", "/projects")
    
    if "error" in result:
        return f"Error retrieving projects: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.resource("todoist://labels")
async def get_labels_resource() -> str:
    """Get a list of all Todoist labels."""
    result = await make_todoist_request("GET", "/labels")
    
    if "error" in result:
        return f"Error retrieving labels: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

# === PROMPTS ===

@mcp.prompt("create_task")
def create_task_prompt(content: str = None, due: str = None, priority: str = None):
    """
    A prompt template for creating a new task in Todoist.
    
    Args:
        content: Task content/description
        due: When the task is due (in natural language)
        priority: Task priority (low, medium, high, very high)
    """
    prompt_text = "Please help me create a new Todoist task"
    
    if all([content, due, priority]):
        prompt_text += f" with these details:\n\nContent: {content}\nDue: {due}\nPriority: {priority}"
    elif content:
        prompt_text += f" with content: {content}"
        if due:
            prompt_text += f" due {due}"
        if priority:
            prompt_text += f" with {priority} priority"
    
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": prompt_text
                }
            }
        ]
    }

@mcp.prompt("plan_project")
def plan_project_prompt(project_name: str = None, goal: str = None):
    """
    A prompt template for planning a new project in Todoist.
    
    Args:
        project_name: Name of the project
        goal: Main goal of the project
    """
    if all([project_name, goal]):
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please help me plan a new Todoist project called '{project_name}' with the main goal: {goal}. Suggest a structure with tasks, due dates, and priorities."
                    }
                }
            ]
        }
    else:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": "I need to plan a new project in Todoist. Can you help me create a structure with tasks, due dates, and priorities?"
                    }
                }
            ]
        }

@mcp.prompt("productivity_report")
def productivity_report_prompt(timeframe: str = None):
    """
    A prompt template for generating a productivity report based on Todoist data.
    
    Args:
        timeframe: Time period for the report (e.g., "this week", "last month")
    """
    if timeframe:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please analyze my Todoist data for {timeframe} and generate a productivity report. Include completed tasks, pending tasks, and suggestions for improvement."
                    }
                }
            ]
        }
    else:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": "Please analyze my Todoist data and generate a productivity report. Include completed tasks, pending tasks, and suggestions for improvement."
                    }
                }
            ]
        }

if __name__ == "__main__":
    print("Starting Todoist MCP server...", file=sys.stderr)
    mcp.run()
