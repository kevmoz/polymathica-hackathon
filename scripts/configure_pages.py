#!/usr/bin/env python3
"""Enable GitHub Pages for the hackathon gallery."""

import json
import time
from urllib.error import HTTPError

from upload_release_assets import NAME, OWNER, api, github_token

PAGES_URL = f"https://api.github.com/repos/{OWNER}/{NAME}/pages"


def main() -> int:
    token = github_token()
    try:
        pages = api(token, "GET", PAGES_URL)
        print(f"GitHub Pages already configured: {pages.get('html_url')}")
        return 0
    except HTTPError as exc:
        if exc.code != 404:
            raise

    payload = {"source": {"branch": "main", "path": "/"}}
    pages = api(token, "POST", PAGES_URL, json.dumps(payload).encode("utf-8"))
    print(f"GitHub Pages configured: {pages.get('html_url')}")
    time.sleep(2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
