# Architecture overview

- Core orchestrates memory, logic, autonomy and evolution.
- Engine contains stateless logic + decision makers.
- Evolver keeps a persistent small model of "score" and can propose actions.
- Storage uses JSON for portability; replace with SQLite/Postgres later.
- Integrations provide safe bridges to old software and system commands.

Security notes:
- System bridge can run commands; limit access to trusted operators.
- When enabling web-facing LLMs, ensure API keys are provided via env.
