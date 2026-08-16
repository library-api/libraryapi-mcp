# libraryapi-mcp

<!-- Links this package to its entry in the official MCP registry -->
mcp-name: dev.libraryapi/libraryapi-mcp

MCP server for [libraryapi.dev](https://libraryapi.dev) — US public library data for AI agents.

Expose library lookups as tools to any MCP-compatible AI assistant (Claude, Cursor, Copilot, etc.). Built on the federal IMLS Public Libraries Survey — public domain, commercially usable.

## Installation

```bash
pip install libraryapi-mcp
```

Or run directly with `uvx` (no install needed):

```bash
uvx libraryapi-mcp
```

## Configuration

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "libraryapi": {
      "command": "uvx",
      "args": ["libraryapi-mcp"],
      "env": {
        "LIBRARYAPI_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Cursor / other MCP clients

```json
{
  "mcpServers": {
    "libraryapi": {
      "command": "uvx",
      "args": ["libraryapi-mcp"],
      "env": {
        "LIBRARYAPI_KEY": "your_api_key_here"
      }
    }
  }
}
```

Get a free API key at [libraryapi.dev](https://libraryapi.dev) — 500 requests/month, no credit card.

## Available Tools

| Tool | Description |
|------|-------------|
| `find_libraries_near_address` | Find the nearest branches to a US street address |
| `find_libraries_near_coordinates` | Same, but from a lat/lng (skips geocoding) |
| `get_outlet` | Full record for one branch outlet by ID |
| `search_libraries` | Search library *systems* by name, state, or city |
| `get_library` | Full system profile by FSCS ID |
| `get_state_summary` | Statewide library totals |

**Systems vs. outlets:** a *system* is the administrative entity (e.g. "Chicago Public Library"); an *outlet* is an individual branch. Proximity searches return outlets.

## Examples

Once configured, you can ask your AI assistant:

> "What are the three closest public libraries to 350 Fifth Ave, New York?"

> "How many public library branches are there in Vermont, and what's the total collection size?"

> "I'm building a civic app — give me every library branch within 5 miles of downtown Chicago as JSON."

## Data note

The IMLS survey covers locations, collections, staffing, visits, programs, and finances. It reports **hours-open totals** (annual, and per week) but **not daily opening times** — so this API can tell you a branch is open ~45 hours/week, not that it opens at 9am.

## Links

- **Website:** [libraryapi.dev](https://libraryapi.dev)
- **PyPI:** [pypi.org/project/libraryapi-mcp](https://pypi.org/project/libraryapi-mcp)
- **REST API docs:** [libraryapi.dev/docs](https://libraryapi.dev/docs)

## License

MIT
