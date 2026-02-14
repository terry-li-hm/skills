# qianli

Search Chinese content platforms from the terminal.

## Trigger

User says "qianli", "chinese search", "search xhs", "search wechat", "search zhihu", "search 36kr", or wants Chinese-language content research.

## User-invocable

Yes. `/qianli`

## Usage

```bash
# Fast CDP sources (direct websocket, 4-18s)
qianli wechat "AI 银行"          # WeChat 公众号 via Sogou
qianli 36kr "大模型 金融"         # 36kr tech news

# MediaCrawler sources (subprocess, 30-60s)
qianli xhs "AI banking"          # Xiaohongshu (requires first-run QR auth)
qianli zhihu "人工智能"           # Zhihu Q&A (requires first-run QR auth)

# Aggregate (wechat + 36kr only, skips slow sources)
qianli all "AI"

# Read page content
qianli read <url>
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--limit` | 5 (3 for `all`) | Max results per source |
| `--json` | false | JSON output instead of text |

## Architecture

Two backends:
- **CDP direct** (wechat, 36kr): Opens tab via CDP websocket, runs JS extractor, closes tab. Fast.
- **MediaCrawler** (xhs, zhihu): Runs `~/code/MediaCrawler` as subprocess with its own venv. Patches `CRAWLER_MAX_NOTES_COUNT` for limit, reads JSON output from temp dir.

## Prerequisites

- CDP Chrome running on port 9222: `open "/Applications/Chrome CDP.app"`
- MediaCrawler installed at `~/code/MediaCrawler` with `.venv`
- XHS/Zhihu: first-run QR auth (see below)

## First-run auth (XHS/Zhihu)

Run once with `--headless false` to scan QR code in browser window:

```bash
cd ~/code/MediaCrawler && .venv/bin/python main.py \
  --platform xhs --type search --keywords "test" --headless false
```

Login state persists in CDP Chrome's profile.

## Gotchas

- `all` runs wechat + 36kr only (xhs/zhihu too slow for aggregation)
- XHS anti-bot: conservative pacing, 1-2 searches/day
- 36kr: heavy SPA, ~12s wait, CAPTCHA after rapid requests
- MediaCrawler patches config file temporarily (restored in finally block)
- Zhihu: may still be unreliable depending on anti-bot state

## Source

- CLI: `~/code/qianli/src/qianli/cli.py`
- MC backend: `~/code/qianli/src/qianli/mc.py`
- MediaCrawler: `~/code/MediaCrawler/`
- Spec: `~/docs/specs/qianli.md`
