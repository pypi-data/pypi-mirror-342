from __future__ import print_function
from mcp.server.fastmcp import FastMCP
import os
import logging
import requests

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

mcp = FastMCP("VeFaaS Browser Use")

@mcp.tool(description="""Creates a browser use task which can automatically browse the web.
Use this when you need to create a browser use task with specific messages.
The endpoint is read from the environment variable BROWSER_USE_ENDPOINT.
The tool will display progress updates during task execution and return the final result.
""")
def create_browser_use_task(task: str):
    # check required environment variables and parameters
    endpoint = os.getenv("BROWSER_USE_ENDPOINT")

    if not endpoint:
        raise ValueError("BROWSER_USE_ENDPOINT is not set")
    
    if not task:
        raise ValueError("Task are required")
    
    if not endpoint.startswith("http://") and not endpoint.startswith("https://"):
        endpoint = f"http://{endpoint}"

    url = f"{endpoint}/tasks"
        
    payload = {
        "messages": [
            {
                "role": "user",
                "content": task
            }
        ]
    }
    
    headers = {
        "X-Faas-Event-Type": "http",
        "Content-Type": "application/json"
    }
    
    try:
        # 1. create a new task
        response = requests.post(url, headers=headers, json=payload)
        
        response.raise_for_status()
        
        response_json = response.json() if response.content else None
        
        task_id = response_json.get("task_id") if response_json else None

        print(f"Task ID: {task_id}")
        
        # Return early if task creation failed or no task_id was returned
        if not task_id:
            return {
                "status_code": response.status_code,
                "response": response_json,
                "error": "No task_id returned from task creation"
            }
        
        # 2. stream the response
        url = f"{endpoint}/tasks/{task_id}/stream"
        response = requests.get(url, stream=True)
        
        response.raise_for_status()
        
        final_content = None
        
        for line in response.iter_lines(decode_unicode=True):
            if line:
                if "choices" in line:
                    return line
                    break
        
    except requests.exceptions.RequestException as e:
        error_message = f"Error in browser use task: {str(e)}"
        raise ValueError(error_message)

def main():
    logger.info("Starting veFaaS browser use MCP Server")
    
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
