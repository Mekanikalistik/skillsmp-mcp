import asyncio
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from mcp.server import MCPServer

server = MCPServer("skillsmp")


def load_api_key() -> str:
    """Resolves the SkillsMP API key from environment variables or local env files."""
    # 1. Direct environment variable
    api_key = os.environ.get("SKILLSMP_API_KEY")
    if api_key:
        return api_key.strip()

    # 2. Candidate env files to look for
    candidate_files = [
        Path.cwd() / ".env",
        Path.cwd() / "skillsmp.env",
        Path.cwd() / "skillsmp_server.env",
        Path(__file__).parent / ".env",
        Path(__file__).parent / "skillsmp.env",
        Path(__file__).parent.parent.parent / ".env",
        Path(__file__).parent.parent.parent / "skillsmp.env",
        Path.home() / ".gemini" / "config" / "skillsmp.env",
    ]

    for env_path in candidate_files:
        if env_path.is_file():
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        if "=" in line:
                            k, v = line.split("=", 1)
                            if k.strip() == "SKILLSMP_API_KEY":
                                val = v.strip().strip("\"'")
                                if val:
                                    return val
            except Exception:
                pass

    return ""


@server.tool()
async def search_skillsmp(
    q: str,
    limit: int = 20,
    sortBy: str = "stars",
    category: str = None,
    language: str = None,
) -> str:
    """Searches the SkillsMP marketplace for agent skills, workflows, and prompts using keywords.

    Args:
        q: The search query or keyword (e.g., 'automation', 'SEO', 'react').
        limit: Number of results to return (default: 20, max: 100).
        sortBy: Sort order of the results ("stars" or "recent").
        category: Optional slug to filter by category (e.g., 'data-ai', 'devops').
        language: ISO code to filter by skill content language (e.g., 'en', 'zh').
    """
    api_key = load_api_key()
    if not api_key:
        return json.dumps(
            {
                "success": False,
                "error": "MISSING_API_KEY",
                "message": (
                    "SKILLSMP_API_KEY is not set. Please set the SKILLSMP_API_KEY "
                    "environment variable in your MCP client configuration or provide a skillsmp.env file. "
                    "You can get an API key at https://skillsmp.com"
                ),
            }
        )

    url = "https://skillsmp.com/api/v1/skills/search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "skillsmp-mcp/0.1.0",
        "Accept": "application/json",
    }

    params = {"q": q, "limit": limit, "sortBy": sortBy}
    if category:
        params["category"] = category
    if language:
        params["language"] = language

    query_string = urllib.parse.urlencode(params)
    full_url = f"{url}?{query_string}"

    req = urllib.request.Request(full_url, headers=headers)
    try:
        loop = asyncio.get_running_loop()

        def fetch_sync():
            with urllib.request.urlopen(req, timeout=15) as response:
                return response.read().decode("utf-8")

        return await loop.run_in_executor(None, fetch_sync)
    except urllib.error.HTTPError as e:
        if e.code == 429:
            return json.dumps({"success": False, "error": "DAILY_QUOTA_EXCEEDED"})
        elif e.code == 401:
            return json.dumps(
                {
                    "success": False,
                    "error": "UNAUTHORIZED",
                    "message": "Invalid SKILLSMP_API_KEY. Please verify your key on https://skillsmp.com",
                }
            )
        elif e.code == 400:
            try:
                body = e.read().decode("utf-8")
            except Exception:
                body = ""
            return json.dumps({"success": False, "error": f"Bad Request: {body}"})
        return json.dumps({"success": False, "error": f"HTTP {e.code}: {e.reason}"})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


@server.tool()
async def fetch_skillsmp_skill(githubUrl: str) -> str:
    """Fetches the full SKILL.md markdown content for a skill using its githubUrl returned from search.

    Args:
        githubUrl: The githubUrl of the skill returned from search_skillsmp.
    """
    if not githubUrl or not githubUrl.startswith("https://github.com/"):
        return json.dumps({"success": False, "error": "Invalid githubUrl"})

    raw_url = (
        githubUrl.replace("https://github.com/", "https://raw.githubusercontent.com/").replace(
            "/tree/", "/"
        )
        + "/SKILL.md"
    )

    req = urllib.request.Request(
        raw_url,
        headers={"User-Agent": "skillsmp-mcp/0.1.0"},
    )

    try:
        loop = asyncio.get_running_loop()

        def fetch_sync():
            with urllib.request.urlopen(req, timeout=15) as response:
                return response.read().decode("utf-8")

        return await loop.run_in_executor(None, fetch_sync)
    except urllib.error.HTTPError as e:
        return json.dumps(
            {
                "success": False,
                "error": f"Failed to fetch SKILL.md (HTTP {e.code}): {raw_url}",
            }
        )
    except Exception as e:
        return json.dumps(
            {"success": False, "error": f"Failed to fetch {raw_url}: {str(e)}"}
        )


async def main():
    await server.run_stdio_async()


def main_cli():
    """CLI entrypoint for uvx/pip execution."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main_cli()
