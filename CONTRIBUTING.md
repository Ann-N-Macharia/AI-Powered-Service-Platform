# Contributing to AfyaPlus Service Platform
## Development workflow

1. Create a feature branch from the current worktree.
2. Keep changes focused on one concern at a time.
3. Validate the relevant FastAPI or Docker commands before opening a PR.
4. Update documentation when behavior or configuration changes.

## Local setup

- Create a `.env` file with your local secrets and never commit it.
- Install Python dependencies for the service or MCP folders you are changing.
- Run the service locally with Uvicorn or Docker Compose.

## Versioning

- Triage API version: `1.1.0`
- Agent image tag: `afyaplus-agent:1.0.0`
- Triage image tag: `afyaplus-triage:1.0.0`

Thanks for helping improve the platform.