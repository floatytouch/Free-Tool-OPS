# Floaty Buddy

Livestream marketing bot for **Floaty Touch** — the "always beside you" companion.

Lineage: BesideYou (personal project: users donate, the bot helps them back when they
struggle) → FocusKey (renamed) → Floaty Buddy (stream bot that markets Floaty Touch and
acquires customers).

## Layout
- `core/`    — bot runtime (stream control via OBS websocket, chat loop)
- `plugins/` — drop-in plugins, one folder each
- `docs/`    — notes and design

## Plugins
Each plugin lives in `plugins/<name>/` with its own `README.md` and entry file.
