---
name: restriction-point
description: Check today's Oura readiness score and recommend appropriate workout intensity
model: sonnet
user-invocable: true
context: fork
---

Check today's exercise readiness. Run `sopor` via Bash to get Oura data. Then:
- Readiness <70: light only (walk, gentle stretch). Flag recovery mode.
- Readiness 70-75: moderate OK (yoga, light weights). Skip high intensity.
- Readiness >75: full intensity cleared.

Check vault health notes (`~/notes/Health/`) for active injuries or medication. Also check `vigilis check-readiness` if available. Return one sentence with readiness score and recommendation.

The nudge: combining readiness thresholds with active health context (medication, injuries, sleep quality) — baseline wouldn't know the thresholds or where to find health notes.
