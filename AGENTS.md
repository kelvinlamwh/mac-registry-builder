# Instructions for LLM Agents

## Project Structure
- Runtime code lives under `src/`.

### Repo overview and instructions (most important first)
- AGENTS.md (this file): Implementation guidelines and best practices for LLM agents.
- README.md: Overview of the project, setup instructions, and usage guidelines.
- PROGRESS-for-agents.md: Ongoing progress updates, open TODO items.
  + Never commit PROGRESS-for-agents.md into the repository. It is for internal use only and should be ignored by git.
  + If PROGRESS-for-agents.md is missing, create it and fill with ongoing tasks and TODOs in checklist form. Nest and/or split items if tasks being overly complex.
  + Without explicit instructions, you may `UPDATE SET checkbox`, `INSERT`, `DELETE WHERE done <> true` for (sub-)items in PROGRESS-for-agents.md in response to repository changes.

## Development Guidelines (most important first)

### Dependencies & Public APIs
- Do NOT add dependencies. You may suggest dependencies, but the user will do the final thing.
- Do NOT change public behavior unless the explicitly asked by the user.

### Developer Workflow
- Use `uv sync` to install or refresh dependencies.
- Use `uv run src/main.py --help` to confirm the CLI wiring after changes.
- Use `uv run --with pyinstaller pyinstaller mac_registry.spec` when validating packaging changes.

### Safe Editing
- Read relevant files before editing.
- Do NOT refactor unrelated code or reformat files without reason.
- If you detect unexpected modifications you did not make, stop and ask the user.
- Make minimal, targeted, and easy to review patches that directly solve the request.
- Write clear, maintainable code. Readability goes first.
- Avoid destructive actions and never discard user changes.

### Python Practices
- Follow existing project style and structure.
- Keep functions focused and names explicit.
- Add brief comments only for non-obvious logic.

### Validation
- Run the smallest useful checks after edits.
- Fix errors introduced by your changes.
- If validation cannot be run, state that clearly.

### Communication
- Summarize what changed and why.
- Reference exact files touched.
- Call out assumptions, risks, and any remaining gaps.