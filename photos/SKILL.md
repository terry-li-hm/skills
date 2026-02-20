# Photos

Access iCloud Photos from Claude Code sessions. Reference skill — not user-invocable.

## When to Use

- User asks to check recent photos, today's photos, or photos from a date
- User wants to view/assess a photo (selfie, screenshot, product shot)
- User says "check my photos", "did the photo sync", "export that photo"

## CLI

```bash
python3 ~/scripts/photos.py <command>
```

| Command | Example | Notes |
|---------|---------|-------|
| `today` | `photos.py today` | Today's photos |
| `recent [N]` | `photos.py recent 5` | Last N photos (default 10, last 7 days) |
| `date YYYY-MM-DD` | `photos.py date 2026-02-20` | Specific date |
| `range FROM TO` | `photos.py range 2026-02-18 2026-02-20` | Date range |
| `export UUID [...]` | `photos.py export E6F41232` | Export to `~/tmp/photos/` as JPEG |
| `search KEYWORD` | `photos.py search "Terry"` | Search descriptions, titles, people |

Output format: `UUID(8) | timestamp | filename | [labels]`

## Workflow

1. **Find the photo:** `recent`, `today`, `date`, or `search`
2. **Export:** `export <8-char-UUID>` — converts HEIC→JPEG to `~/tmp/photos/`
3. **View:** `Read` tool on the exported JPEG path

## Gotchas

- **iCloud sync lag:** iPhone says "synced" but Mac DB may not have it yet. Run `open -a Photos` to trigger sync, wait 30-60s, then recheck.
- **`[iCloud]` tag** = photo not downloaded locally. Export falls back to derivative JPEG (2048px) — usually fine for viewing. Original unavailable until downloaded in Photos.app.
- **Short UUIDs work:** 8-char prefix resolved via SQL LIKE. No need for full UUID.
- **Photos.app must not be open for DB writes** but read-only access (what we do) is always safe.
- **Screen sleeping (headless SSH):** `screencapture` of Photos.app returns black. Use `export` + `Read` instead.

## Direct sips bypass

If the script has issues, convert manually:
```bash
sips -s format jpeg -s formatOptions 92 "<Photos Library>/originals/{UUID_PREFIX}/{FULL_UUID}.heic" --out ~/tmp/photos/output.jpeg
```

## Architecture

- Zero dependencies — direct SQLite on `~/Pictures/Photos Library.photoslibrary/database/Photos.sqlite`
- Core Data epoch (2001-01-01), ZASSET table, read-only mode
- Person names via ZDETECTEDFACE → ZPERSON join
- <0.1s per query (was 47s with osxphotos)
