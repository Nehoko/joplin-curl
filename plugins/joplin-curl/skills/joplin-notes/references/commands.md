# Joplin Curl Commands

## Config

- Helper path: set `JOPLIN_API_PY=/absolute/path/to/joplin_api.py`
- Default config path: `data/joplin-config.json` under the plugin root containing the helper's `scripts/` directory
- Stored keys: `base_url`, `port`, `token`
- `show-config` masks the token in terminal output.

## Commands

```bash
python3 "$JOPLIN_API_PY" set-config --base-url URL --port PORT --token TOKEN
python3 "$JOPLIN_API_PY" show-config
python3 "$JOPLIN_API_PY" ping
python3 "$JOPLIN_API_PY" list-notebooks [--limit N]
python3 "$JOPLIN_API_PY" search --query TEXT [--type note|folder|tag] [--fields a,b,c] [--limit N]
python3 "$JOPLIN_API_PY" get-note --note-id NOTE_ID [--fields a,b,c]
python3 "$JOPLIN_API_PY" create-note --title TITLE [--body TEXT] [--parent-id NOTEBOOK_ID]
python3 "$JOPLIN_API_PY" update-note --note-id NOTE_ID [--title TITLE] [--body TEXT] [--parent-id NOTEBOOK_ID]
python3 "$JOPLIN_API_PY" request --method GET|POST|PUT|DELETE --path /endpoint [--query a=b] [--data '{"x":"y"}' | --data-file body.json]
```

## Notes

- All API requests use `curl`.
- `request` accepts repeated `--query key=value` flags.
- `request` accepts either inline JSON with `--data` or a file path with `--data-file`.
- The helper raises an error on non-2xx responses and prints the response body when possible.
