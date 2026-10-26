#!/usr/bin/env python3
"""Serve the stream overlays on loopback only (OBS browser sources cannot render file:// reliably)."""
from __future__ import annotations

import argparse
import logging
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 18793


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, format: str, *args) -> None:
        logging.info("%s - %s", self.address_string(), format % args)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()
    if args.host not in ("127.0.0.1", "::1"):
        raise SystemExit("refusing to bind outside loopback")

    if not ROOT.is_dir():
        raise SystemExit(f"missing overlay root: {ROOT}")

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    logging.info("stream-kit http://%s:%s/ -> %s", args.host, args.port, ROOT)
    server.serve_forever()


if __name__ == "__main__":
    main()
