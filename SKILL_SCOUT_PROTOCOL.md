# Skill Scout Protocol (SkillsMP)

You have access to the SkillsMP marketplace via MCP tools (`search_skillsmp` and `fetch_skillsmp_skill`). 
Follow this protocol to ensure you find the most useful skills without bloating your context with redundant information ("word salad").

## When to Trigger
- **Fresh Planning Sessions:** The ideal time to trigger the scout is in a fresh chat session using a large context window model, during initial project planning and brainstorming—before any code is written or issues are introduced.
- **Proactive:** If you are starting a new architecture, or lack a clear runbook for a requested tech stack, you MUST proactively look for relevant skills.
- **Reactive:** If the user asks you to "scout for skills" based on a project description.

## The 4-Step Smart Workflow

### 1. Autonomous Keyword Generation
- Analyze the user's high-level project description and tech stack.
- You must autonomously deduce the technical direction. Generate highly specific, long-tail keywords (e.g., `"Next.js 14 App Router caching patterns"` or `"Supabase RLS strict policies"`). Do not use generic terms.
- Run `search_skillsmp` using these smart keywords.
- *Crucial:* Cast a wide net for *relevant* skills. Do not assume you already know a skill just by its title. You cannot judge a skill before you read it.

### 2. Fetch and Evaluate
- For the most promising results returned by the search, use `fetch_skillsmp_skill(githubUrl)` to read their actual `SKILL.md` content.
- **The "Word Salad" Filter:** Rigorously evaluate the fetched content against your innate knowledge.
  - **Reject:** Skills that only contain standard syntax, generic advice, or basic boilerplate.
  - **Keep:** Skills that contain novel runbooks, specific undocumented APIs, complex integration architectures, or strict checklists.

### 3. Justification & Consultation
- Before saving any skills to the file system, present your findings to the user.
- Highlight the skills that passed the filter.
- **Justify:** Explain *exactly why* the project needs each skill and how it fills gaps in your standard knowledge.
- Ask the user to approve the installation of these skills.

### 4. Scoping & Installation
Once the user approves a skill, ask them where to install it, or suggest the best location:
- **Project-Specific (`[PROJECT_ROOT]/.agents/skills/<name>/SKILL.md`):** For tech-stack specific skills (e.g., a specific database schema pattern for this app).
- **Universal (`~/.gemini/config/skills/<name>/SKILL.md` or `~/.claude/skills/...`):** For general workflows (e.g., advanced Git conflict resolution).
Save the `SKILL.md` content to the appropriate directory.
