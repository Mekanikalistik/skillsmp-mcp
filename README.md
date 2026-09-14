# SkillsMP MCP Server 🌐⚡

[![MCP Compatible](https://img.shields.io/badge/MCP-Standard%20Stdio-blue.svg)](https://modelcontextprotocol.io)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://python.org)
[![Zero-Setup uvx](https://img.shields.io/badge/Zero--Setup-uvx-purple.svg)](https://astral.sh/uv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that connects your favorite AI agents and IDEs directly to the **[SkillsMP](https://skillsmp.com)** marketplace.

It enables LLMs (Claude, Gemini, GPT-4, Cursor, Antigravity, Windsurf) to **autonomously search** for curated agent skills, best practices, and workflows, then **fetch the exact `SKILL.md` instructions** on demand.

---

## 🛡️ Critical Directive: Read & Audit Before You Trigger

> ### ⚠️ *"Knowing nothing about the skill you trigger is worse than blind vibe coding."*

In the era of autonomous AI agents, **Agent Skills are executable knowledge**. They don't merely provide reference documentation—they define system heuristics, tool execution rules, architectural constraints, and operational boundaries for your AI agent.

### Why Blind Skill Execution is Dangerous:
* **Vibe Coding vs. Skill Poisoning**: If you blindly "vibe code", an LLM might generate a buggy snippet that fails a compiler or test run. But if you blindly inject an unvetted `SKILL.md` into your agent's runtime, you **corrupt the agent's reasoning engine** with outdated APIs, antipatterns, or conflicting directives that taint every subsequent task in your workspace.
* **The "Word Salad" Hazard**: Many skills published on public marketplaces are generic boilerplate or copied API signatures. Injecting these wastes valuable context window tokens and degrades reasoning performance without offering actionable runbooks.
* **Permission & Action Exposure**: Real agent skills often define terminal execution patterns, file modifications, or infrastructure interactions. Triggering a skill without knowing what it does compromises reproducibility and project safety.

### 📋 The 3-Point Audit Checklist Before Adopting Any Skill:
1. **Inspect the `SKILL.md`**: Always review the prompt triggers, step-by-step instructions, and expected tool calls before running it.
2. **Filter Out Generic Boilerplate**: If a skill just tells the model things standard foundation models already know (like basic syntax), discard it. Prioritize skills with novel runbooks, battle-tested workflows, or strict compliance steps.
3. **Scope Responsibly**: Prefer isolated, project-level scoping (`.agents/skills/<name>/`) instead of universally polluting your global agent configuration.

---

## 🤖 1-Prompt Auto-Install for Your AI Agent

Don't want to configure JSON files manually? Copy and paste this prompt directly into your AI assistant (Google Antigravity, Cursor, Claude, Windsurf, or Roo Code):

```text
Please configure the SkillsMP MCP server and its Skill Scout rule from https://github.com/Mekanikalistik/skillsmp-mcp for me:
1. Add "skillsmp" to my MCP server configuration using command "uvx" with args ["--from", "git+https://github.com/Mekanikalistik/skillsmp-mcp.git", "skillsmp-mcp"] and env {"SKILLSMP_API_KEY": "PASTE_KEY_HERE"}.
2. Download SKILL_SCOUT_PROTOCOL.md from the repo and save it to my agent rules/skills directory so you know how to scout, filter out "word salad", and ask for confirmation before installing skills.
3. Prompt me to paste my API key from https://skillsmp.com if I haven't already.
```

---

## ⚡ Zero-Setup Execution via `uvx` (Manual Setup)

No manual git clone, virtual environments, or dependency management required! If you have [uv](https://docs.astral.sh/uv/) installed, you can run the server directly:

```bash
uvx --from git+https://github.com/Mekanikalistik/skillsmp-mcp.git skillsmp-mcp
```

---

## 🔌 One-Click Client Configuration

Add this server to your AI tool of choice. Just make sure to provide your `SKILLSMP_API_KEY`.

### 1. Claude Desktop
Add to `claude_desktop_config.json`:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "skillsmp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/Mekanikalistik/skillsmp-mcp.git",
        "skillsmp-mcp"
      ],
      "env": {
        "SKILLSMP_API_KEY": "sk_live_skillsmp_your_api_key_here"
      }
    }
  }
}
```

### 2. Cursor
Add to your project's `.cursor/mcp.json` or Global Cursor Settings:

```json
{
  "mcpServers": {
    "skillsmp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/Mekanikalistik/skillsmp-mcp.git",
        "skillsmp-mcp"
      ],
      "env": {
        "SKILLSMP_API_KEY": "sk_live_skillsmp_your_api_key_here"
      }
    }
  }
}
```

### 3. Google Antigravity / Gemini IDE
Add to `~/.gemini/config/mcp_config.json`:

```json
{
  "mcpServers": {
    "skillsmp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/Mekanikalistik/skillsmp-mcp.git",
        "skillsmp-mcp"
      ],
      "env": {
        "SKILLSMP_API_KEY": "sk_live_skillsmp_your_api_key_here"
      },
      "disabled": false
    }
  }
}
```

### 4. Windsurf / Roo Code / Cline
Configure as a Stdio MCP server:
- **Command**: `uvx`
- **Arguments**: `["--from", "git+https://github.com/Mekanikalistik/skillsmp-mcp.git", "skillsmp-mcp"]`
- **Environment**: `{"SKILLSMP_API_KEY": "your_api_key_here"}`

---

## 🔑 API Key Configuration

You can provide your SkillsMP API key in any of these ways:

1. **Environment Variable (Best Practice)**:
   Pass `SKILLSMP_API_KEY` in your MCP client's `env` block.
2. **Local Environment File**:
   Copy `.env.example` or `skillsmp.env.template` to `.env` or `skillsmp.env`:
   ```bash
   cp skillsmp.env.template skillsmp.env
   ```
   Edit the file:
   ```ini
   SKILLSMP_API_KEY=sk_live_skillsmp_your_actual_key
   ```
   The server automatically detects `.env`, `skillsmp.env`, and `~/.gemini/config/skillsmp.env`.

> 💡 **Where to get a key?** Register or sign in at [skillsmp.com](https://skillsmp.com) to generate your live API token.

---

## 🛠️ How It Works & Available Tools

```
               ┌───────────────────────┐
               │    LLM / AI Agent     │
               └───────────┬───────────┘
                           │ (stdio JSON-RPC)
               ┌───────────▼───────────┐
               │      skillsmp-mcp     │
               └───┬───────────────┬───┘
                   │               │
  search_skillsmp  │               │ fetch_skillsmp_skill
                   ▼               ▼
      ┌──────────────────────┐   ┌──────────────────────────┐
      │ skillsmp.com REST API │   │ raw.githubusercontent.com│
      │   (Search Marketplace)│   │   (Download SKILL.md)    │
      └──────────────────────┘   └──────────────────────────┘
```

The MCP server exposes two specialized tools:

### 1. `search_skillsmp`
Discovers skills in the SkillsMP marketplace using keywords.

* **API Endpoint**: `GET https://skillsmp.com/api/v1/skills/search`
* **Authentication**: `Authorization: Bearer <SKILLSMP_API_KEY>`
* **Parameters**:
  | Parameter | Type | Required | Default | Description |
  |-----------|------|----------|---------|-------------|
  | `q` | `string` | **Yes** | — | Search query or keywords (e.g., `'Next.js caching'`, `'Docker security'`, `'Postgres RLS'`) |
  | `limit` | `integer` | No | `20` | Maximum results to return (up to `100`) |
  | `sortBy` | `string` | No | `"stars"` | Sort order: `"stars"` or `"recent"` |
  | `category` | `string` | No | `None` | Filter by category slug (e.g., `'devops'`, `'data-ai'`, `'frontend'`) |
  | `language` | `string` | No | `None` | ISO language code (e.g., `'en'`, `'zh'`) |

* **Response Handling**:
  - `200 OK`: Returns matching skills with titles, descriptions, stars, tags, and repository `githubUrl`.
  - `401 Unauthorized`: Returns error prompting the user to verify their API key.
  - `429 Too Many Requests`: Returns `{"error": "DAILY_QUOTA_EXCEEDED"}`.

### 2. `fetch_skillsmp_skill`
Retrieves the raw markdown instructions (`SKILL.md`) for any discovered skill.

* **Parameters**:
  | Parameter | Type | Required | Description |
  |-----------|------|----------|-------------|
  | `githubUrl` | `string` | **Yes** | The GitHub URL returned in `search_skillsmp` (e.g. `https://github.com/user/repo/tree/main/skills/auth`) |

* **URL Transformation**:
  The tool converts:
  `https://github.com/{owner}/{repo}/tree/{branch}/{path}`
  into:
  `https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}/SKILL.md`
  and downloads the full markdown document.

---

## 🧠 Autonomous Agent Protocol (`SKILL_SCOUT_PROTOCOL`)

To help AI assistants use these tools effectively without bloating prompt context, we include a battle-tested rule: [SKILL_SCOUT_PROTOCOL.md](SKILL_SCOUT_PROTOCOL.md).

It instructs agents to:
1. **Generate Specific Keywords**: Avoid generic terms like `"python"`; use targeted long-tail phrases like `"FastAPI JWT refresh rotation"`.
2. **Apply the "Word Salad" Filter**: Read the fetched `SKILL.md` and reject boilerplate, keeping only actionable, novel runbooks.
3. **Consult & Scope**: Ask the user before saving the skill to project-specific (`.agents/skills/`) or global directories.

---

## 💻 Manual / Local Development

If you wish to run or develop the server locally without `uvx`:

```bash
# Clone the repository
git clone https://github.com/Mekanikalistik/skillsmp-mcp.git
cd skillsmp-mcp

# Run with uv
uv run skillsmp-mcp

# Or standard pip
pip install -e .
python -m skillsmp_mcp.server
```

---

## 📄 License

Distributed under the [MIT License](LICENSE).
