---
name: str-relabelling
description: STR relabelling project (FR-MLP-002) — deployment checklist, safety checks, gotchas. Use when working on STR relabelling handover or CDSW deployment.
user_invocable: true
---

# STR Relabelling (FR-MLP-002)

## Key References

- **Handover doc:** `[[STR Relabelling Handover]]`
- **Progress note:** `[[STR Relabelling Implementation Progress]]`
- **Local repo:** `~/code/str-relabelling/`
- **Implementation spec:** `~/code/str-relabelling/docs/implementation-spec.md`
- **Pipeline test gist:** https://gist.github.com/terry-li-hm/66d27d3007a776723087751f0f7ea974

## Deployment Checklist

### 1. Apply patch (2 files)

**`conf/base/parameters.yml`** — add:
```yaml
termination_str_status:
  - '21'
  - '24'
```

**`data_preprocessing/nodes.py`** — paste block from `implementation_patch.py` after line 1669.

### 2. Safety checks before running Kedro

**Check A — Catalog outputs:**
```bash
grep -r "imh_apm_core" conf/base/catalog.yml conf/local/catalog.yml
```
No output = Kedro won't write to production.

**Check B — Inline writes (bypass catalog):**
```bash
grep -n -i "insert\|overwrite\|create table\|write\|save\|to_parquet\|to_csv" src/apm/pipelines/data_preprocessing/nodes.py | grep -v ":\s*#" | head -20
```
Excludes comment lines. No hits inside `preprocess_strs` = safe.

**Known write functions in this file:**
- `save_to_hive_table` at lines ~1788 and ~2325 — both OUTSIDE `preprocess_strs` (which ends ~line 1770). These are called by other nodes in the pipeline.

### 3. Run integration test

**Safe (no writes):**
```python
from src.apm.pipelines.data_preprocessing.nodes import preprocess_strs
print("Import OK")
```

**Kedro — use `--node` only, NOT `--pipeline`:**
```bash
kedro run --node=preprocess_strs
```
**DO NOT use `--pipeline=data_preprocessing`** — other nodes in the pipeline call `save_to_hive_table` which writes to Hive. `--node=preprocess_strs` runs only the one function.

### 4. Validate

Run `pipeline_node_test.py` — expect:
- Row count stable (~828,112)
- Relabel count ~14,881 (±500)
- "ALL PASSED"

## Critical Gotchas

- **`alert_typ_id` is NOT in `imh_apm_core.str`.** Do not filter on it. Pipeline filters for system alerts (10007) upstream. Earlier versions of the patch had this filter — it would crash with `KeyError`.
- **`alert_stat` is string, not int** — use `'21'`, `'24'`, `'25'`
- **`alert_dt` needs `pd.to_datetime()`** on data from raw table
- **Appeal data (status 18) must come from raw table** (`dsp_iol.imh_tb_iadtm_sam_alert`), not `imh_apm_core.str` — model table misses post-disposition appeals
- **`spark_read_sql` needs 3 args in production:** `(query, "app_name", ConnectionMode.HWC)` — test scripts use simplified 1-arg version
- **Status 35 doesn't exist yet** — add to YAML after O25-07 go-live (June 2026)
- **Standalone test scripts load their own data** — they JOIN `alert_typ_id` from raw table, masking that the column doesn't exist in the model table. Test passing ≠ production code works. See `~/docs/solutions/patterns/standalone-test-data-masking.md`
- **`save_to_hive_table` exists in `nodes.py` but outside `preprocess_strs`** — other pipeline nodes write to Hive. Always use `kedro run --node=preprocess_strs`, never `--pipeline=data_preprocessing`

## Remaining Work

- [ ] Fill `[TODO:]` sections in handover doc (CDSW paths, change procedure, contacts)
- [ ] Formal IT change procedure before production
- [ ] Share handover with successor (due Mar 13)

## Timeline

- Jan 22: Playground test (200k sample) — 6,447 relabelled
- Jan 27: Marco Round 1 spot check
- Feb 9: Marco Round 2 (appeal exclusion fix) — all 8 samples confirmed
- Feb 10: Codebase audit — only 2 files need changes
- Feb 23: Dry run passed, pipeline node test passed (828,112 rows, 14,881 relabelled)
- Feb 23: Fixed alert_typ_id bug (would have crashed in production)
