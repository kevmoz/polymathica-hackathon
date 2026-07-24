#!/usr/bin/env python3
"""Upload prepared release assets using the current Git credential helper."""

import json
import mimetypes
import subprocess
import sys
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

REPO = "kevmoz/polymathica-hackathon"
OWNER, NAME = REPO.split("/", 1)
TAG = "v1.0.0-hackathon"
TITLE = "POLYMATHICA Hackathon Submission"
NOTES = "Complete autonomous scientific laboratory with real GPU-accelerated simulations"
ASSET_DIR = Path("release_assets")


def github_token() -> str:
    request = "protocol=https\nhost=github.com\n\n"
    result = subprocess.run(
        ["git", "credential", "fill"],
        input=request,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    fields = {}
    for line in result.stdout.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            fields[key] = value
    token = fields.get("password")
    if not token:
        raise RuntimeError("Git credential helper did not return a GitHub token/password")
    return token


def api(token: str, method: str, url: str, data: bytes | None = None, content_type: str = "application/json"):
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "User-Agent": "polymathica-release-uploader",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if data is not None:
        headers["Content-Type"] = content_type
    request = Request(url, data=data, headers=headers, method=method)
    with urlopen(request) as response:
        body = response.read()
        if not body:
            return None
        return json.loads(body.decode("utf-8"))


def get_or_create_release(token: str) -> dict:
    release_url = f"https://api.github.com/repos/{OWNER}/{NAME}/releases/tags/{TAG}"
    try:
        return api(token, "GET", release_url)
    except HTTPError as exc:
        if exc.code != 404:
            raise

    payload = {
        "tag_name": TAG,
        "target_commitish": "main",
        "name": TITLE,
        "body": NOTES,
        "draft": False,
        "prerelease": False,
    }
    create_url = f"https://api.github.com/repos/{OWNER}/{NAME}/releases"
    return api(token, "POST", create_url, json.dumps(payload).encode("utf-8"))


def delete_existing_asset(token: str, release: dict, asset_name: str) -> None:
    for asset in release.get("assets", []):
        if asset.get("name") == asset_name:
            api(token, "DELETE", asset["url"])
            print(f"Deleted existing asset: {asset_name}")


def upload_asset(token: str, release: dict, asset_path: Path) -> None:
    delete_existing_asset(token, release, asset_path.name)
    upload_url = release["upload_url"].split("{", 1)[0]
    url = f"{upload_url}?{urlencode({'name': asset_path.name})}"
    content_type = mimetypes.guess_type(asset_path.name)[0] or "application/octet-stream"
    api(token, "POST", url, asset_path.read_bytes(), content_type=content_type)
    print(f"Uploaded asset: {asset_path.name}")


def main() -> int:
    assets = sorted(ASSET_DIR.glob("*.mp4"))
    if not assets:
        print(f"No .mp4 assets found in {ASSET_DIR}", file=sys.stderr)
        return 1

    token = github_token()
    release = get_or_create_release(token)
    print(f"Release ready: {release['html_url']}")

    for asset in assets:
        upload_asset(token, release, asset)

    print(f"Uploaded {len(assets)} assets to {release['html_url']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
