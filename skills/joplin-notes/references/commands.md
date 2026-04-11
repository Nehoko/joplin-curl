# Joplin Curl Commands

## Config

- Default config path: `/Users/iliamikhailov/work/plugins/joplin-curl/data/joplin-config.json`
- Stored keys: `base_url`, `port`, `token`
- `show-config` masks the token in terminal output.

## Commands

```bash
python3 /Users/iliamikhailov/work/plugins/joplin-curl/scripts/joplin_api.py set-config --base-url URL --port PORT --token TOKEN
python3 /Users/iliamikhailov/work/plugins/joplin-curl/scripts/joplin_api.py show-config
python3 /Users/iliamikhailov/work/plugins/joplin-curl/scripts/joplin_api.py ping
python3 /Users/iliamikhailov/work/plugins/joplin-curl/scripts/joplin_api.py list-notebooks [--limit N]
python3 /Users/iliamikhailov/work/plugins/joplin-curl/scripts/joplin_api.py search --query TEXT [--type note|folder|tag] [--fields a,b,c] [--limit N]
python3 /Users/iliamikhailov/work/plugins/joplin-curl/scripts/joplin_api.py get-note --note-id NOTE_ID [--fields a,b,c]
python3 /Users/iliamikhailov/work/plugins/joplin-curl/scripts/joplin_api.py create-note --title TITLE [--body TEXT] [--parent-id NOTEBOOK_ID]
python3 /Users/iliamikhailov/work/plugins/joplin-curl/scripts/joplin_api.py update-note --note-id NOTE_ID [--title TITLE] [--body TEXT] [--parent-id NOTEBOOK_ID]
python3 /Users/iliamikhailov/work/plugins/joplin-curl/scripts/joplin_api.py request --method METHOD --path /endpoint [--query a=b] [--data '{"x":"y"}']
```

## Notes

- All API requests use `curl`.
- `request` accepts repeated `--query key=value` flags.
- `request` accepts either inline JSON with `--data` or a file path with `--data-file`.
- The helper raises an error on non-2xx responses and prints the response body when possible.
