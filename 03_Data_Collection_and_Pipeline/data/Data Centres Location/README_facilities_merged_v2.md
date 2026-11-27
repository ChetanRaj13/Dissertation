# README: `facilities_merged_v2.json`

Data dictionary for the India data-centre facilities dataset.

> **How this was written.** Everything below was derived by inspecting the file itself (field names, types, value distributions, example records). The file ships with no schema, so where a meaning is an **inference** from how a field is used rather than a documented definition, it is marked *(inferred)*. Counts are for this version of the file (89 records).

---

## 1. What the dataset is

A single JSON file holding **one array of 89 flat records** (no nesting inside a record). Each record describes one of the following: a data-centre facility or campus, a sub-component of a facility, a company-wide programme, a state or national roll-up, or a row that was **excluded** from the dataset after review (kept for audit).

Every record has the same 23 keys. Missing information is stored as `null`, never as an empty string.

```json
{
  "id": "F34",
  "record_type": "child",
  "parent_id": "F32",
  "facility_name": "Reliance-Meta anchor facility (Jamnagar)",
  "operator": "Reliance Industries (Meta as lessee)",
  "state": "Gujarat",
  "city": "Jamnagar",
  "cap_operational_mw": null,
  "cap_ultimate_mw": 168,
  "cap_basis": "facility (Reliance release)",
  "status": "Agreement signed; under development",
  "workload_class": "AI-specific (explicitly stated)",
  "year": 2028,
  "year_type": "target_delivery",
  "year_note": "Release dated 10 Jun 2026 says delivered within two years.",
  "as_of": "2026-06",
  "power_procurement": "Renewable energy supplied and managed by RIL; Meta separately backing ~1 GW RE via CleanMax and Fourth Partner Energy",
  "cooling_water": "Desalinated seawater",
  "investment": null,
  "sum_ok": false,
  "verification": "verified-primary (Reliance release, ril.com)",
  "source": "https://www.ril.com/...",
  "notes": "Meta leases capacity under a long-term agreement, with an option to scale. Nested inside F32."
}
```

---

## 2. Read this first: the dataset is not a census, and capacities must not be naively summed

- Facility-level data for India is patchy. Most records have **no capacity figure** (74 of 89 have no operational MW; 48 of 89 have no ultimate MW).
- Several records **overlap** (a campus, the phase inside it, and a company-wide programme that includes both). Adding every MW value will **double-count**.
- Roll-up and programme rows are **reference/context rows**, not additional capacity.
- Use the `sum_ok` flag (section 5) to decide what is safe to add, and read `cap_basis` to see what each MW number actually measures.

---

## 3. Record types (`record_type`)

| Value | Count | Meaning | Typical ID prefix |
|---|---|---|---|
| `facility` | 56 | A data-centre site, campus, region or phase treated as a standalone entry. | `F`, `N` |
| `child` | 8 | A component of, or nested within, another record (a phase, a region, an anchor facility). | `F`, `N` |
| `programme` | 3 | A company-wide or multi-site commitment/target with no single location (e.g., an "India-wide target"). `state`/`city` = `Multiple`. | `F`, `N` |
| `state_rollup` | 10 | A directional summary for one state (facility counts, city-level MW from trackers). No capacity fields filled; details sit in `notes`. | `S` |
| `national_rollup` | 1 | The all-India directional summary (`state` = `National Total`). | `S` |
| `excluded` | 11 | A row from an earlier source that was **rejected** after checking. `notes` records the original claim and the reason. Keep out of analysis. | `X` |

### ID prefixes (`id`)

- `S` = roll-ups (`S01`–`S11`), `X` = excluded rows (`X01`–`X11`). These follow directly from `record_type`.
- `F` (41 records) and `N` (26 records) are two separate numbering series for facility-type records. The file does not say what the difference is *(inferred: likely different merge batches or source passes)*. Treat the prefix as an opaque identifier; do not filter on it.

### Parent/child links (`parent_id`)

Only 7 records carry a `parent_id`. Existing links:

| Parent | Children |
|---|---|
| `F30` (Vizag AI hub) | `F31` |
| `F32` (Reliance Jamnagar Phase 1) | `F33` (3 GW master plan), `F34` (Meta anchor facility) |
| `N16` (Reliance Visakhapatnam) | `N17` |
| `F39` (AWS India commitment, 670 MW) | `F40`, `F41`, `F42` |

Quirks worth knowing:
- `F39` has `record_type = "child"` but **no** `parent_id`. It is the umbrella for `F40`–`F42` (its note says 670 = 400 + 120 + 150).
- Nesting is by **scope, not strict hierarchy**. `F33` (the 3 GW master plan) is listed as a child of `F32` (Phase 1) but its note says it *contains* Phase 1, and `F34` is nested inside both. Never sum parent and child together.

---

## 4. Field dictionary

"Filled" = records with a non-null value (out of 89).

### Identification

| Field | Type | Filled | Description |
|---|---|---|---|
| `id` | string | 89 | Unique record key (`F01`, `N16`, `S03`, `X08`...). Used by `parent_id` and referenced inside `notes`. |
| `record_type` | string (enum) | 89 | Kind of record. See section 3. |
| `parent_id` | string or null | 7 | `id` of the record this one is nested under. |
| `facility_name` | string | 89 | Name of the facility, campus, phase or programme. **Not unique**: every `state_rollup` row is literally named "State rollup". Use `id` as the key. |
| `operator` | string | 89 | Operating company or developer (43 distinct values). Can carry qualifiers, e.g., `STT (probable; statewise table said NTT)` or `Reliance Industries (Meta as lessee)`. Multi-party records list several names. |

### Location

| Field | Type | Filled | Description |
|---|---|---|---|
| `state` | string | 89 | Indian state. Special values: `Multiple` (programmes), `National Total` (the national roll-up). Rows in `excluded` keep the location as originally filed, marked `(as filed)`, e.g., `Uttar Pradesh (as filed)`. Clean with `str.replace(" (as filed)", "")` before grouping. |
| `city` | string | 89 | City or locality, free text (50 distinct), often with a sub-area in brackets, e.g., `Kolkata (New Town)`. Roll-ups use descriptive text such as `Chennai-led`. Not standardised. |

### Capacity (MW)

All values are numeric megawatts (int or float). The **basis differs row to row**, so always read `cap_basis`.

| Field | Type | Filled | Description |
|---|---|---|---|
| `cap_operational_mw` | number or null | 15 | Capacity reported as **live/operating** today. Often a minimum, e.g., only the first building of a campus. `null` means not disclosed or not found, **not** zero. |
| `cap_ultimate_mw` | number or null | 41 | Planned, announced or full build-out capacity. Can be a campus target, an approved allocation, a tracker estimate or an aspiration. |
| `cap_basis` | string or null | 45 | What the MW figures measure and where they come from (34 distinct free-text values). Examples: `IT load`, `critical IT load`, `announced`, `MoU`, `tracker (Wikipedia)`, `tracker allocation`, `aspirational target (Blackridge)`, `state approval order`, `approximate (press)`. Treat `tracker`, `announced`, `MoU` and `aspirational` bases as weaker than company-stated IT load. |

### Status and workload

| Field | Type | Filled | Description |
|---|---|---|---|
| `status` | string or null | 78 | Development stage. Free text with ~31 variants. Main groups: `Operational` (incl. phase 1, expanding, mixed), `Under construction`, `Planned`, `Approved`, `Announced`, `MoU stage`, `Under evaluation`, and `Mixed` (roll-ups). Some values carry caveats, e.g., `Under construction (go-live was targeted Aug 2026; not confirmed)`. `null` on all 11 `excluded` rows. |
| `workload_class` | string or null | 78 | Type of computing workload. 16 variants; main groups below. `null` on all 11 `excluded` rows. |

`workload_class` groups:

| Group | Values in the file | Notes |
|---|---|---|
| General | `General/Colocation`, `General/Hyperscale`, `General/Cloud`, `General/Enterprise Cloud`, `Government/General` | Conventional workloads. |
| AI-confirmed | `AI-specific (explicitly stated)`, `AI-specific (cloud/AI region)`, `AI-specific (frontier AI)`, `AI-native/Hyperscale` | The operator or a primary source says AI. |
| AI-ready / uncertain | `AI-ready/Hyperscale`, `General/AI-ready`, `General/AI-ready mix`, `Hyperscale (AI-specific unconfirmed)`, `Hyperscale` | Capable of AI or hyperscale, but AI use **not** confirmed. Do not count as AI load without a stated assumption. |
| Other | `Mixed` (roll-ups), `Unclassified` | |

### Timing

| Field | Type | Filled | Description |
|---|---|---|---|
| `year` | integer or null | 18 | A single year tied to the facility. **Its meaning depends on `year_type`.** `null` for 71 records. |
| `year_type` | string (enum) | 89 | What `year` represents: `operational_since` (8), `target_first_phase` (3), `announced` (3), `target_go_live` (2), `target_delivery` (1), `target_completion` (1), `not_disclosed` (71). Always populated, so use it to tell actual dates from targets. |
| `year_note` | string or null | 18 | Evidence or caveat for the year, e.g., "Phase 1 was targeted for March 2024; exact go-live date not found." Mostly filled where `year` is filled (16 rows have both), but two rows with a `year` have no note, and two rows with `year = null` have a note explaining why (e.g., "Delivery year not found."). |
| `as_of` | string or null | 16 | Date of the information snapshot, format `YYYY-MM` (range 2024-01 to 2026-09). Filled for 16 records only; most rows have no snapshot date. |

### Energy, water and money (sparse; mostly flagship projects)

| Field | Type | Filled | Description |
|---|---|---|---|
| `power_procurement` | string or null | 7 | How the site gets (or plans to get) power: renewable PPAs, captive solar, sanctioned grid load, etc. Free text as reported. |
| `cooling_water` | string or null | 6 | Cooling approach / water source as reported, e.g., `Liquid cooling`, `Desalinated seawater`, `Zero-water cooling reported (press), not confirmed...`. Free text; some entries are explicitly unconfirmed. |
| `investment` | string or null | 13 | Reported investment as **text**, with mixed currencies and units (`US$15 bn`, `Rs 16,466 crore`, `about Rs 1.6 lakh crore total`, `up to Rs 70,000 crore`). Not normalised to a common currency; some are ranges or "up to". |

### Data quality and provenance

| Field | Type | Filled | Description |
|---|---|---|---|
| `sum_ok` | boolean | 89 | Whether the row's MW figures may be added into a total. `true` (30) vs `false` (59). **All 30 `true` rows are `facility` records**; roll-ups, programmes, children and excluded rows are always `false`. Facility rows are `false` where capacity is missing, conflicting, unconfirmed, or nested inside another record *(inferred from usage; the file has no definition of the flag)*. |
| `verification` | string | 89 | How well the row is backed (32 free-text variants). Main groups below. |
| `source` | string | 89 | Where the row came from. 43 are URLs; 46 are plain-text citations, e.g., `Wikipedia: List of data centres in West Bengal`, `WRI India + OCOLO + Arizton (2026)`. Several rows list multiple sources separated by `;`. |
| `notes` | string or null | 76 | Analyst commentary: site size, merge decisions, conflicts between sources, warnings such as "Do not sum", and for `excluded` rows the original claim plus the reason for exclusion. Cross-references use `id` values. |

`verification` groups (strongest to weakest):

| Group | Meaning |
|---|---|
| `verified-primary (...)` | Company release, government order or similar primary document located. |
| `verified-secondary (...)` | Reported by reputable secondary sources (press, trade sites, DCD). Primary document not obtained. |
| `cross-checked (...)` | Two or more tracker/reference sources agree (e.g., Wikipedia + DCD). |
| `single-source` | One source only (some with qualifiers, e.g., existence confirmed, MW unconfirmed). Largest group (25+). |
| `directional only` | Used for roll-ups; indicative, not precise. |
| `unverified-conflict (...)` / `unverified-low-quality source` | Sources disagree, or the only source is weak. Use with caution. |
| `excluded` | Row was rejected; do not use. |

---

## 5. Recommended usage

1. **Filter by record type first.** Facility-level analysis: `record_type == "facility"`. Drop `excluded` rows entirely.
2. **Sum only what is safe:** `record_type == "facility"` and `sum_ok == true`. Even then, check `cap_basis` because IT load, facility load and tracker estimates are not like-for-like.
3. **Keep operational and planned apart.** Do not add `cap_operational_mw` and `cap_ultimate_mw` of the same row; `ultimate` normally already includes the operational part.
4. **Interpret `year` through `year_type`.** Only `operational_since` is a historical fact; the others are targets or announcements.
5. **Treat `null` as "unknown".** A missing MW value does not mean zero capacity, and a missing `as_of` does not mean the data is current.
6. **Roll-ups are for cross-checking**, not for adding to facility totals.

```python
import json
import pandas as pd

df = pd.DataFrame(json.load(open("facilities_merged_v2.json")))

# Facility rows whose MW can be safely added
safe = df[(df.record_type == "facility") & (df.sum_ok)]
print(safe[["cap_operational_mw", "cap_ultimate_mw"]].sum(min_count=1))

# Strip the "(as filed)" suffix before grouping by state
df["state_clean"] = df["state"].str.replace(" (as filed)", "", regex=False)
```

---

## 6. Known limitations

- **Not a census.** Capacity is missing for most facilities, and trackers disagree on counts and sizes.
- **Free-text categories.** `status`, `workload_class`, `cap_basis`, `verification`, `operator` and `city` are not controlled vocabularies; group them (e.g., by prefix) before counting.
- **Mixed measurement bases** for MW (IT load vs facility load vs tracker estimate vs aspiration).
- **Investment is unstructured text** in mixed currencies.
- **`F`/`N` ID series, `sum_ok` and the parent/child semantics** are not documented in the file; the interpretations above are inferred from usage.
- **Time-sensitive.** Most records have no `as_of` date; the latest snapshot in the file is 2026-09.
