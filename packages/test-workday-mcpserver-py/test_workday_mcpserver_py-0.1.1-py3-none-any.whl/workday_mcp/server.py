# server.py
from mcp.server.fastmcp import FastMCP, Context
import requests
import sys
import json
import traceback
from typing import Dict, Any, List
from .utils.env_validator import env_validator
from datetime import datetime

# Capture stderr for diagnostics
import io
import contextlib

# Create an MCP server
mcp = FastMCP("Workday")


@mcp.tool()
def get_workday_workers(ctx: Context) -> Dict[str, Any]:
    """
    Fetch workers from Workday API using the access token from environment
    
    Args:
        ctx: MCP context for logging
    
    Returns:
        Dict[str, Any]: Response from Workday API containing worker information
    """
    url = "https://wd2-impl-services1.workday.com/ccx/api/staffing/v6/ibmsrv_pt1/workers/"
    
    try:
        # Get validated access token from environment
        access_token = env_validator.get_access_token()
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        ctx.log.error(f"Error fetching workers from Workday API: {str(e)}")
        return {"error": f"Error fetching workers: {str(e)}"}


@mcp.tool()
def get_worker_eligible_absence_types(worker_id: str, ctx: Context) -> Dict[str, Any]:
    """
    Fetch eligible absence types for a specific worker
    
    Args:
        worker_id (str): The ID of the worker to fetch absence types for
        ctx: MCP context for logging
    
    Returns:
        Dict[str, Any]: Response from Workday API containing eligible absence types
    """
    
    base_url = "https://wd2-impl-services1.workday.com/ccx/api/absenceManagement/v2/ibmsrv_pt1"
    url = f"{base_url}/workers/{worker_id}/eligibleAbsenceTypes"
    
    try:
        # Get validated access token from environment
        access_token = env_validator.get_access_token()
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        params = {
            "limit": 100
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        ctx.log.error(f"Error fetching eligible absence types for worker {worker_id}: {str(e)}")
        return {"error": f"Error fetching eligible absence types: {str(e)}"}


@mcp.tool()
def request_time_off(worker_id: str, date: str, daily_quantity: str, time_off_type_id: str, ctx: Context) -> Dict[str, Any]:
    """
    Submit a time off request for a worker
    
    Args:
        worker_id (str): The ID of the worker requesting time off
        date (str): The date for the time off request in ISO format (e.g., "2025-02-28T17:00:00.000Z")
        daily_quantity (str): The amount of time off requested (e.g., "1" for full day)
        time_off_type_id (str): The ID of the time off type
        ctx: MCP context for logging
    
    Returns:
        Dict[str, Any]: Response from Workday API containing the request result
    """
    base_url = "https://wd2-impl-services1.workday.com/ccx/api/absenceManagement/v2/ibmsrv_pt1"
    url = f"{base_url}/workers/{worker_id}/requestTimeOff"
    
    try:
        # Get validated access token from environment
        access_token = env_validator.get_access_token()
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "days": [
                {
                    "date": date,
                    "dailyQuantity": daily_quantity,
                    "timeOffType": {
                        "id": time_off_type_id
                    }
                }
            ]
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        ctx.log.error(f"Error requesting time off for worker {worker_id}: {str(e)}")
        return {"error": f"Error requesting time off: {str(e)}"}


def main():
    # Redirect stdout to stderr to avoid contaminating the JSON output
    real_stdout = sys.stdout
    sys.stdout = sys.stderr
    
    try:
        # Log diagnostic information to stderr only
        print("Starting Workday MCP server...", file=sys.stderr)
        
        # Run the MCP server with the original stdout restored
        sys.stdout = real_stdout
        mcp.run()
    except Exception as e:
        # Print any errors to stderr to help with debugging
        print(f"Error in Workday MCP server: {str(e)}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        sys.exit(1)
    finally:
        # Restore stdout
        sys.stdout = real_stdout


if __name__ == "__main__":
    main()