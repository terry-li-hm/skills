# Kindle Extractor Skill

## Trigger
`/kindle`, "kindle extract", "extract book", "scrape kindle"

## What This Does
Starts a background extraction of the currently open Kindle book in agent-browser.
Uses `kindle-extract` CLI (at `~/bin/kindle-extract`) which:
- Auto-detects the book title from the tab
- Auto-resumes from the last extracted page
- Saves to `~/notes/Books/<title>.md`
- Uses Gemini 2.5 Flash-Lite vision to transcribe each page

## Steps

### 1. Verify agent-browser is on Kindle
```bash
agent-browser get url
```
Output must contain `read.amazon.com`. If not, tell the user to open Kindle Cloud Reader first.

### 2. Get book title and check existing output
```bash
agent-browser get title
```
Parse title: "AWAKENINGS | Kindle" → "Awakenings" → `~/notes/Books/Awakenings.md`

Check if file exists and how many pages are already extracted:
```bash
/usr/bin/grep -c "--- Page" ~/notes/Books/<title>.md 2>/dev/null || echo "0"
```

Report to user: "Found 46 pages already extracted — will resume from page 47."

### 3. Start extraction backgrounded
```bash
nohup kindle-extract > ~/tmp/kindle-<safe_title>.log 2>&1 &
echo $!
```

**Important:** Use `safe_title` (spaces replaced with hyphens, lowercased) for the log file.

### 4. Report to user

```
Starting extraction of "Awakenings" in background (PID: 12345)
Output: ~/notes/Books/Awakenings.md
Resume: 46 pages already done, continuing from page 47

Monitor progress:
  tail -f ~/tmp/kindle-awakenings.log

Stop extraction:
  kill 12345
```

## Notes
- If `nohup` output file already exists, it will be appended to (safe — kindle-extract itself handles resume)
- The log file shows per-page progress: `Page 47/559 (8%)... done (1,243 chars)`
- Extraction rate is ~2.5s/page (limited by page render wait) → ~23 min per 559 pages
- Default model is `gemini-2.5-flash-lite` — fast and cheap for OCR tasks
- To use a different model: `nohup kindle-extract --model gemini-2.0-flash > ... &`
- To stop at a specific page: `nohup kindle-extract --end-page 100 > ... &`

## Files
- CLI: `~/bin/kindle-extract`
- Output: `~/notes/Books/`
- Logs: `~/tmp/kindle-<title>.log`
