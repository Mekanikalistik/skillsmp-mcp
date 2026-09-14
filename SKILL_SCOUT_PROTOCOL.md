# Skill Scout Protocol (SkillsMP)

You have access to the SkillsMP marketplace via MCP tools (`search_skillsmp` and `fetch_skillsmp_skill`). 
Follow this protocol to ensure you find the most useful skills without bloating your context with redundant information ("word salad").

## When to Trigger
- **Proactive:** If you are stuck on a complex bug, starting a project with an unfamiliar tech stack, or lacking a clear runbook for a requested task, you MUST proactively look for relevant skills.
- **Reactive:** If the user explicitly asks you to find skills, scout for skills, or says they will trigger the scout.

## The 4-Step Smart Workflow

### 1. Smart Keyword Generation
- Analyze the project's tech stack and the specific problem.
- Generate highly specific, long-tail keywords (e.g., `"Next.js 14 App Router caching patterns"` or `"Supabase RLS strict policies"`). Do not use generic terms like `"React"` or `"Python"`.
- Run `search_skillsmp` using these smart keywords.
- *Crucial:* Cast a wide net for *relevant* skills. Do not assume you already know a skill just by its title or metadata. You cannot judge a skill before you read it.

### 2. Fetch and Evaluate
- For the most promising results returned by the search, use `fetch_skillsmp_skill(githubUrl)` to read their actual `SKILL.md` content.
- **The "Word Salad" Filter:** Rigorously evaluate the fetched content against your innate knowledge.
  - **Reject:** Skills that only contain standard syntax, generic advice, or basic boilerplate.
  - **Keep:** Skills that contain novel runbooks, specific undocumented APIs, complex integration architectures, or strict checklists.

### 3. Consultation Session
- Before saving any skills to the file system, present your findings to the user.
- Highlight 1-3 skills that passed the filter.
- Explain *exactly why* the skill is useful (e.g., "It provides a 5-step checklist for secure authentication").
- Ask the user if they want to install the skill and where it should be scoped.

### 4. Scoping & Installation
Once the user approves a skill, ask them where to install it, or suggest the best location:
- **Project-Specific (`[PROJECT_ROOT]/.agents/skills/<name>/SKILL.md`):** For tech-stack specific skills (e.g., a specific database schema pattern for this app).
- **Universal (`~/.gemini/config/skills/<name>/SKILL.md` or `~/.claude/skills/...`):** For general workflows (e.g., advanced Git conflict resolution).
Save the `SKILL.md` content to the appropriate directory.
