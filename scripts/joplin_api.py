#!/usr/bin/env python3

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, List, Optional, Tuple
from urllib.parse import urlencode


PLUGIN_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = PLUGIN_ROOT / "data" / "joplin-config.json"


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def load_config(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        fail(
            "Joplin config missing. Run `set-config` first with --base-url, --port, and --token."
        )

    try:
        payload = json.loads(config_path.read_text())
    except json.JSONDecodeError as exc:
        fail(f"Invalid config JSON in {config_path}: {exc}")

    for key in ("base_url", "port", "token"):
        if not payload.get(key):
            fail(f"Config field `{key}` missing in {config_path}")

    return payload


def save_config(config_path: Path, base_url: str, port: int, token: str) -> None:
    config_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "base_url": base_url.rstrip("/"),
        "port": port,
        "token": token,
    }
    config_path.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"Saved config to {config_path}")


def masked_token(token: str) -> str:
    if len(token) <= 8:
        return "*" * len(token)
    return f"{token[:4]}...{token[-4:]}"


def build_url(config: dict[str, Any], path: str, query_items: List[Tuple[str, str]]) -> str:
    normalized_path = path if path.startswith("/") else f"/{path}"
    query = list(query_items)
    query.append(("token", str(config["token"])))
    query_string = urlencode(query, doseq=True)
    return f'{config["base_url"]}:{config["port"]}{normalized_path}?{query_string}'


def run_curl(method: str, url: str, data: Optional[str] = None) -> str:
    command = ["curl", "--silent", "--show-error", "--fail-with-body", "-X", method.upper(), url]
    if data is not None:
        command.extend(["-H", "Content-Type: application/json", "--data", data])

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        if result.stdout.strip():
            print(result.stdout.strip(), file=sys.stderr)
        if result.stderr.strip():
            print(result.stderr.strip(), file=sys.stderr)
        raise SystemExit(result.returncode)

    return result.stdout


def parse_query_items(values: Optional[List[str]]) -> List[Tuple[str, str]]:
    items: List[Tuple[str, str]] = []
    for value in values or []:
        if "=" not in value:
            fail(f"Invalid query item `{value}`. Expected key=value.")
        key, item_value = value.split("=", 1)
        items.append((key, item_value))
    return items


def print_json(raw: str) -> None:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        print(raw)
        return

    print(json.dumps(payload, indent=2))


def cmd_set_config(args: argparse.Namespace) -> None:
    save_config(args.config, args.base_url, args.port, args.token)


def cmd_show_config(args: argparse.Namespace) -> None:
    payload = load_config(args.config)
    payload["token"] = masked_token(str(payload["token"]))
    print(json.dumps(payload, indent=2))


def cmd_ping(args: argparse.Namespace) -> None:
    config = load_config(args.config)
    url = build_url(config, "/ping", [])
    output = run_curl("GET", url)
    print(output.strip())


def cmd_list_notebooks(args: argparse.Namespace) -> None:
    config = load_config(args.config)
    query = [("fields", "id,parent_id,title"), ("limit", str(args.limit))]
    url = build_url(config, "/folders", query)
    print_json(run_curl("GET", url))


def cmd_search(args: argparse.Namespace) -> None:
    config = load_config(args.config)
    query = [("query", args.query), ("limit", str(args.limit))]
    if args.type:
        query.append(("type", args.type))
    if args.fields:
        query.append(("fields", args.fields))
    url = build_url(config, "/search", query)
    print_json(run_curl("GET", url))


def cmd_get_note(args: argparse.Namespace) -> None:
    config = load_config(args.config)
    query: List[Tuple[str, str]] = []
    if args.fields:
        query.append(("fields", args.fields))
    url = build_url(config, f"/notes/{args.note_id}", query)
    print_json(run_curl("GET", url))


def cmd_create_note(args: argparse.Namespace) -> None:
    config = load_config(args.config)
    payload: dict[str, Any] = {"title": args.title}
    if args.body is not None:
        payload["body"] = args.body
    if args.parent_id:
        payload["parent_id"] = args.parent_id
    url = build_url(config, "/notes", [])
    print_json(run_curl("POST", url, json.dumps(payload)))


def cmd_update_note(args: argparse.Namespace) -> None:
    config = load_config(args.config)
    payload: dict[str, Any] = {}
    if args.title is not None:
        payload["title"] = args.title
    if args.body is not None:
        payload["body"] = args.body
    if args.parent_id is not None:
        payload["parent_id"] = args.parent_id
    if not payload:
        fail("Nothing to update. Provide at least one of --title, --body, or --parent-id.")
    url = build_url(config, f"/notes/{args.note_id}", [])
    print_json(run_curl("PUT", url, json.dumps(payload)))


def cmd_request(args: argparse.Namespace) -> None:
    config = load_config(args.config)
    query = parse_query_items(args.query)
    data = args.data
    if args.data_file:
        data = Path(args.data_file).read_text()
    url = build_url(config, args.path, query)
    print_json(run_curl(args.method, url, data))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Joplin Data API helper backed by curl.")
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help=f"Config file path. Defaults to {DEFAULT_CONFIG_PATH}",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    set_config = subparsers.add_parser("set-config", help="Persist Joplin connection settings.")
    set_config.add_argument("--base-url", required=True, help="Base URL, for example http://127.0.0.1")
    set_config.add_argument("--port", required=True, type=int, help="Clipper port, for example 41184")
    set_config.add_argument("--token", required=True, help="Joplin API token")
    set_config.set_defaults(func=cmd_set_config)

    show_config = subparsers.add_parser("show-config", help="Show saved settings with a masked token.")
    show_config.set_defaults(func=cmd_show_config)

    ping = subparsers.add_parser("ping", help="Check that the clipper API responds.")
    ping.set_defaults(func=cmd_ping)

    list_notebooks = subparsers.add_parser("list-notebooks", help="List notebooks.")
    list_notebooks.add_argument("--limit", type=int, default=100)
    list_notebooks.set_defaults(func=cmd_list_notebooks)

    search = subparsers.add_parser("search", help="Search notes, folders, or tags.")
    search.add_argument("--query", required=True)
    search.add_argument("--type", choices=["note", "folder", "tag"])
    search.add_argument("--fields", help="Comma-separated Joplin fields")
    search.add_argument("--limit", type=int, default=20)
    search.set_defaults(func=cmd_search)

    get_note = subparsers.add_parser("get-note", help="Fetch a note by ID.")
    get_note.add_argument("--note-id", required=True)
    get_note.add_argument("--fields", help="Comma-separated Joplin fields")
    get_note.set_defaults(func=cmd_get_note)

    create_note = subparsers.add_parser("create-note", help="Create a note.")
    create_note.add_argument("--title", required=True)
    create_note.add_argument("--body")
    create_note.add_argument("--parent-id")
    create_note.set_defaults(func=cmd_create_note)

    update_note = subparsers.add_parser("update-note", help="Update a note.")
    update_note.add_argument("--note-id", required=True)
    update_note.add_argument("--title")
    update_note.add_argument("--body")
    update_note.add_argument("--parent-id")
    update_note.set_defaults(func=cmd_update_note)

    request = subparsers.add_parser("request", help="Run a generic Joplin API request.")
    request.add_argument("--method", required=True, choices=["GET", "POST", "PUT", "DELETE"])
    request.add_argument("--path", required=True, help="API path, for example /notes")
    request.add_argument("--query", action="append", help="Repeatable key=value query item")
    request.add_argument("--data", help="Inline JSON request body")
    request.add_argument("--data-file", help="Path to a JSON request body file")
    request.set_defaults(func=cmd_request)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
