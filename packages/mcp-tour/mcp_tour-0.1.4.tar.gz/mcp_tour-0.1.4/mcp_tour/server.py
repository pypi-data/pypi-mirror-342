"""
Korea Tourism Organization API integration for Claude using MCP protocol.

This module provides tools to access Korea Tourism Organization's tourism data API
through the MCP (Model Control Protocol) interface.
"""

import os
import sys
from dotenv import load_dotenv
import json
import httpx
from fastmcp import FastMCP
from typing import Optional
from httpx import HTTPTransport

# Load environment variables from .env file
load_dotenv()

mcp = FastMCP(
    "Korea Tourism API",
    description="Access Korea Tourism Organization's tourism data API",
    dependencies=[
        "httpx",
        "python-dotenv",
        "pydantic"
    ]
)

TOUR_API_KEY = os.environ.get("TOUR_API_KEY")
if not TOUR_API_KEY:
    raise ValueError("TOUR_API_KEY environment variable is not set")
    
API_ENDPOINT = "https://apis.data.go.kr/B551011/TarRlteTarService"

# Transport configuration
transport = HTTPTransport(verify=False)

@mcp.tool(
    name="get_area_based_list",
    description="Get tourist spots information based on area from Korea Tourism Organization",
)
async def get_area_based_list(
    area_code: str,
    content_type_id: Optional[str] = None,
    size: int = 50,
) -> str:
    """
    Get area-based tourist spots information from Korea Tourism Organization API.
    
    Args:
        area_code (str): Area code for the region
        content_type_id (str, optional): Content type ID (12: Tourist Spots, 39: Restaurants, 32: Accommodation)
        size (int): Number of results to return (max 50)
        
    Returns:
        str: JSON response containing tourist spot information
        
    Raises:
        Exception: If API request fails
    """
    async with httpx.AsyncClient(transport=transport, verify=False) as client:
        try:
            params = {
                "serviceKey": TOUR_API_KEY,
                "areaCode": area_code,
                "numOfRows": min(size, 50),
                "_type": "json"
            }
            if content_type_id:
                params["contentTypeId"] = content_type_id

            response = await client.get(
                f"{API_ENDPOINT}/areaBasedList",
                params=params,
                timeout=30.0
            )
            
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error in get_area_based_list: {str(e)}", file=sys.stderr)
            raise

@mcp.tool(
    name="search_by_keyword",
    description="Search tourist spots by keyword from Korea Tourism Organization",
)
async def search_by_keyword(
    keyword: str,
    content_type_id: Optional[str] = None,
    size: int = 50,
) -> str:
    """
    Search tourist spots by keyword from Korea Tourism Organization API.
    
    Args:
        keyword (str): Search keyword
        content_type_id (str, optional): Content type ID (12: Tourist Spots, 39: Restaurants, 32: Accommodation)
        size (int): Number of results to return (max 50)
        
    Returns:
        str: JSON response containing search results
        
    Raises:
        Exception: If API request fails
    """
    async with httpx.AsyncClient(transport=transport, verify=False) as client:
        try:
            params = {
                "serviceKey": TOUR_API_KEY,
                "keyword": keyword,
                "numOfRows": min(size, 50),
                "_type": "json"
            }
            if content_type_id:
                params["contentTypeId"] = content_type_id

            response = await client.get(
                f"{API_ENDPOINT}/searchKeyword",
                params=params,
                timeout=30.0
            )
            
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error in search_by_keyword: {str(e)}", file=sys.stderr)
            raise

if __name__ == "__main__":
    mcp.run()