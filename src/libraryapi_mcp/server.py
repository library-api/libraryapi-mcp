"""
libraryapi MCP server — exposes US public library data as MCP tools.

Configure with environment variable:
  LIBRARYAPI_KEY=your_api_key

Run via uvx:
  uvx libraryapi-mcp
"""

import os
import httpx
from mcp.server.fastmcp import FastMCP

BASE_URL = os.environ.get("LIBRARYAPI_BASE_URL", "https://api.libraryapi.dev")
API_KEY = os.environ.get("LIBRARYAPI_KEY", "")

mcp = FastMCP(
    "libraryapi",
    instructions=(
        "Use these tools to look up US public libraries — both library systems "
        "and their individual branch outlets. Data comes from the federal IMLS "
        "Public Libraries Survey. The most useful tool is "
        "find_libraries_near_address, which returns the nearest branches to any "
        "US address. Note: this data covers locations, collections, staffing, "
        "visits, and programs — it does NOT include daily opening times."
    ),
)


def _headers() -> dict:
    if not API_KEY:
        raise ValueError(
            "LIBRARYAPI_KEY environment variable is not set. "
            "Get a free API key at https://libraryapi.dev"
        )
    return {"X-API-Key": API_KEY, "Accept": "application/json"}


def _get(path: str, params: dict | None = None) -> dict:
    with httpx.Client(base_url=BASE_URL, headers=_headers(), timeout=15) as client:
        response = client.get(path, params=params)
        response.raise_for_status()
        return response.json()


# ---------------------------------------------------------------------------
# Proximity search
# ---------------------------------------------------------------------------

@mcp.tool()
def find_libraries_near_address(
    address: str,
    radius_miles: float = 10.0,
    limit: int = 10,
    include_closed: bool = False,
) -> dict:
    """
    Find the public library branches nearest to a US street address,
    sorted by distance.

    Args:
        address:        Full US street address, e.g. "350 Fifth Ave, New York, NY"
        radius_miles:   Search radius in miles (0.1–50, default 10)
        limit:          Maximum branches to return (1–100, default 10)
        include_closed: Include temporarily-closed branches (default False)
    """
    return _get("/v1/outlets", params={
        "address": address,
        "radius_miles": radius_miles,
        "limit": limit,
        "include_closed": include_closed,
    })


@mcp.tool()
def find_libraries_near_coordinates(
    lat: float,
    lng: float,
    radius_miles: float = 10.0,
    limit: int = 10,
    include_closed: bool = False,
) -> dict:
    """
    Find the public library branches nearest to a latitude/longitude, sorted by
    distance. Use this when you already have coordinates; it skips geocoding and
    is faster than find_libraries_near_address.

    Args:
        lat:            Latitude (WGS84)
        lng:            Longitude (WGS84)
        radius_miles:   Search radius in miles (0.1–50, default 10)
        limit:          Maximum branches to return (1–100, default 10)
        include_closed: Include temporarily-closed branches (default False)
    """
    return _get("/v1/outlets", params={
        "lat": lat,
        "lng": lng,
        "radius_miles": radius_miles,
        "limit": limit,
        "include_closed": include_closed,
    })


# ---------------------------------------------------------------------------
# Lookup and browse
# ---------------------------------------------------------------------------

@mcp.tool()
def get_outlet(outlet_id: str) -> dict:
    """
    Get the full record for one library branch (outlet) by its ID, including
    address, phone, coordinates, and service details.

    Args:
        outlet_id: IMLS outlet ID
    """
    return _get(f"/v1/outlets/{outlet_id}")


@mcp.tool()
def search_libraries(name: str = "", state: str = "", city: str = "", limit: int = 20, offset: int = 0) -> dict:
    """
    Search public library *systems* by name, state, and/or city. A system is the
    administrative entity (e.g. "Chicago Public Library") that operates one or
    more branch outlets. Provide at least one of name, state, or city.

    Args:
        name:   Library system name (full-text search)
        state:  Two-letter state code, e.g. "IL"
        city:   City name (substring match)
        limit:  Results per page (1–100, default 20)
        offset: Pagination offset (default 0)
    """
    params: dict = {"limit": limit, "offset": offset}
    for key, value in (("name", name), ("state", state.upper()), ("city", city)):
        if value:
            params[key] = value
    if not any((name, state, city)):
        raise ValueError("Provide at least one of: name, state, or city.")
    return _get("/v1/libraries/search", params=params)


@mcp.tool()
def get_library(fscs_id: str) -> dict:
    """
    Get the full profile for a library system by its FSCS ID, including
    collections, staffing, visits, programs, and finances.

    Args:
        fscs_id: IMLS FSCS ID for the library system, e.g. "IL0021"
    """
    return _get(f"/v1/libraries/{fscs_id}")


@mcp.tool()
def get_state_summary(state_code: str) -> dict:
    """
    Get statewide public library totals — systems, branch outlets, collections,
    and usage — for one state.

    Args:
        state_code: Two-letter state abbreviation, e.g. "IL"
    """
    return _get(f"/v1/states/{state_code.upper()}/summary")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    mcp.run()


if __name__ == "__main__":
    main()
