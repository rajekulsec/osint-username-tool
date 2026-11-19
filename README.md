# OSINT Username Tool

Check where a username exists across public sites — one command, one table.

## What it does

Looks up a username on GitHub, GitLab, Reddit, Medium, Dev.to, CodePen, HackerOne, YouTube, TikTok, Twitch, Pinterest, Tumblr, Steam and X, and reports FOUND / NOT FOUND / UNKNOWN for each, with the profile link for every hit.

Some sites block automated checks or always return HTTP 200 — those results are clearly marked "verify manually". **Always open a found profile yourself before trusting it.**

## Install

```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 osint-username.py johndoe
python3 osint-username.py johndoe --json results.json
```

Example output:

```
OSINT username lookup — johndoe
============================================================
GitHub       FOUND  https://github.com/johndoe
Reddit       NOT FOUND
YouTube      FOUND  https://www.youtube.com/@johndoe
X (Twitter)  UNKNOWN  (X blocks automated checks — open the link manually)

Found on 2 site(s), unknown/blocked on 1 site(s).
```

## ⚠️ Rules

This tool only reads **public** profile pages. Never use it to harass, stalk or dox anyone. Respect each site's terms of use and rate limits.

## License

MIT
