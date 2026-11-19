#!/usr/bin/env python3
"""osint-username.py — Check where a username exists across public sites.

Usage:
    python3 osint-username.py johndoe
    python3 osint-username.py johndoe --json results.json

Checks public profile pages only. Some sites block automated checks
or always return 200 — those results are marked "verify manually".
Never use this to harass, stalk or dox anyone.
"""

import argparse
import json
import sys
import time

import requests

VERSION = "1.0.0"
HEADERS = {
    "User-Agent": ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"),
    "Accept-Language": "en-US,en;q=0.9",
}
TIMEOUT = 10
DELAY = 0.4

# name, profile URL template, check method
# method "status": 404 means the profile does not exist
# method ("marker", text): page containing the text means "not found"
SITES = [
    ("GitHub", "https://github.com/{u}", "status"),
    ("GitLab", "https://gitlab.com/{u}", "status"),
    ("Reddit", "https://www.reddit.com/user/{u}/", "status"),
    ("Medium", "https://medium.com/@{u}", "status"),
    ("Dev.to", "https://dev.to/{u}", "status"),
    ("CodePen", "https://codepen.io/{u}", "status"),
    ("HackerOne", "https://hackerone.com/{u}", "status"),
    ("YouTube", "https://www.youtube.com/@{u}",
     ("marker", "This channel does not exist")),
    ("TikTok", "https://www.tiktok.com/@{u}",
     ("marker", "Couldn't find this account")),
    ("Twitch", "https://www.twitch.tv/{u}", "status"),
    ("Pinterest", "https://www.pinterest.com/{u}/", "status"),
    ("Tumblr", "https://{u}.tumblr.com/", "status"),
    ("Steam", "https://steamcommunity.com/id/{u}",
     ("marker", "The specified profile could not be found")),
    ("X (Twitter)", "https://x.com/{u}", "manual"),
]


def check_site(session, name, url, method):
    """Return (status, note) where status is FOUND / NOT FOUND / UNKNOWN."""
    if method == "manual":
        return "UNKNOWN", "X blocks automated checks — open the link manually"
    try:
        r = session.get(url, timeout=TIMEOUT, allow_redirects=True)
    except requests.RequestException as exc:
        return "UNKNOWN", f"request failed: {exc.__class__.__name__}"
    if r.status_code in (403, 429):
        return "UNKNOWN", f"blocked by the site (HTTP {r.status_code})"
    if method == "status":
        if r.status_code == 404:
            return "NOT FOUND", ""
        if r.status_code == 200:
            return "FOUND", "verify manually — some sites return 200 always"
        return "UNKNOWN", f"unexpected HTTP {r.status_code}"
    kind, marker = method
    if kind == "marker":
        if marker in r.text:
            return "NOT FOUND", ""
        if r.status_code == 200:
            return "FOUND", "verify manually"
        return "UNKNOWN", f"unexpected HTTP {r.status_code}"
    return "UNKNOWN", "unknown check method"


def main():
    parser = argparse.ArgumentParser(
        description="Check where a username exists across public sites.")
    parser.add_argument("username", help="Username to look up")
    parser.add_argument("--json", dest="json_out",
                        help="Write the results to a JSON file")
    args = parser.parse_args()

    username = args.username.strip().lstrip("@")
    session = requests.Session()
    session.headers.update(HEADERS)

    print(f"\nOSINT username lookup — {username} (osint-username {VERSION})")
    print("=" * 60)
    results = []
    for name, template, method in SITES:
        url = template.format(u=username)
        status, note = check_site(session, name, url, method)
        results.append({"site": name, "url": url,
                        "status": status, "note": note})
        line = f"{name:<12} {status}"
        if status == "FOUND":
            line += f"  {url}"
        if note:
            line += f"  ({note})"
        print(line)
        time.sleep(DELAY)

    found = [r for r in results if r["status"] == "FOUND"]
    unknown = [r for r in results if r["status"] == "UNKNOWN"]
    print(f"\nFound on {len(found)} site(s), "
          f"unknown/blocked on {len(unknown)} site(s).")
    print("Always verify FOUND results by opening the profile yourself.")
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(results, fh, indent=2)
        print(f"JSON results written to {args.json_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
