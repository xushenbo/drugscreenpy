# Drug Screening

This tutorial shows the current substance-level drug-screening workflow in
`drugscreenpy`. The API ports the first end-to-end slice from the
`original/` research code into `drugscreenpy.tl`.

## What the current port covers

- normalize raw therapy rows into prescription rows
- optionally apply structured `drugprepr`-style duration cleaning
- collapse prescriptions into exposure episodes
- build matched exposed and unexposed windows
- screen disease events with a self-controlled cohort design

The current implementation works with structured dosage fields such as
`duration`, `numdays`, `dose_duration`, or `ndd`, and it can also derive
approximate `ndd` values from common free-text dosage instructions such as
`1-2 tablets twice daily` or `every other day`. For more complex instructions,
prefer precomputed structured dosage fields.

The screening wrappers also expose the three workflow variants used in
`original/`: `workflow="actual"`, `workflow="30days"`, and `workflow="365days"`.

## EHRData-first workflow

```python
import ehrdata as ed
import pandas as pd
import drugscreenpy as eds

therapy = pd.DataFrame(
    {
        "patid": [1, 2, 3],
        "eventdate": ["2020-01-10", "2020-01-10", "2020-01-10"],
        "drugsubstance": ["drug_a", "drug_a", "drug_a"],
        "duration": [5, 5, 5],
    }
)

patients = pd.DataFrame(
    {
        "patid": [1, 2, 3],
        "dob": ["1970-01-01", "1970-01-01", "1970-01-01"],
        "frd": ["2019-01-01", "2019-01-01", "2019-01-01"],
        "tod": ["2021-01-01", "2021-01-01", "2021-01-01"],
        "lcd": ["2021-01-01", "2021-01-01", "2021-01-01"],
        "deathdate": ["2021-01-01", "2021-01-01", "2021-01-01"],
    }
)

events = pd.DataFrame(
    {
        "patid": [1, 2, 3],
        "disease": ["disease_x", "disease_x", "disease_x"],
        "disease_eventdate": pd.to_datetime(["2020-01-12", "2020-01-06", "2020-01-13"]),
    }
)

edata = ed.EHRData(obs=patients.set_index("patid"))
eds.tl.set_table(edata, "therapy", therapy)
eds.tl.set_table(edata, "events", events)

result = eds.tl.screen_substance_therapy(
    edata,
    workflow="actual",
    min_total_events=2,
)

result[["drug", "disease", "age.group", "IRR", "p.value"]]
```

`EHRData` is the recommended workflow object. `drugscreenpy` uses `edata.obs`
as the patient or cohort table. Relational drug-screening inputs stay in
`edata.uns["drugscreenpy"]["tables"]`, and output tables are stored in
`edata.uns["drugscreenpy"]["results"]`.

The matrix slots `.X`, `.layers`, `.var`, and `.tem` are not used for raw
therapy, event, or indication tables because those tables are not aligned
feature matrices.

## Standalone DataFrame workflow

The same workflow can also be run directly on pandas DataFrames:

```python
result = eds.tl.screen_substance_therapy(
    therapy,
    patients,
    events,
    workflow="actual",
    min_total_events=2,
)

result[["drug", "disease", "age.group", "IRR", "p.value"]]
```

## OMOP-derived EHRData

If `edata` was created with `ehrdata.io.omop.setup_obs(...)`, use the patient
identifier available in `.obs`, for example `patient_col="person_id"`:

```python
eds.tl.set_table(edata, "therapy", therapy)
eds.tl.set_table(edata, "events", events)

result = eds.tl.screen_substance_therapy(
    edata,
    patient_col="person_id",
    therapy_key="therapy",
    events_key="events",
    min_total_events=2,
)
```

## Matching the original workflow variants

Use the `workflow` argument to match the original script families:

```python
actual_result = eds.tl.screen_substance_therapy(
    therapy,
    patients,
    events,
    workflow="actual",
    min_total_events=2,
)

thirty_day_result = eds.tl.screen_substance_therapy(
    therapy,
    patients,
    events,
    workflow="30days",
    min_total_events=2,
)

year_result = eds.tl.screen_substance_therapy(
    therapy,
    patients,
    events,
    workflow="365days",
    min_total_events=2,
)
```

## Grouped workflow examples

Use `eds.tl.screen_grouped_therapy(...)` when you want to aggregate prepared
prescriptions by BNF hierarchy instead of screening at the substance level.

```python
grouping = pd.DataFrame(
    {
        "prodcode": [10, 11, 20],
        "bnf.section": ["section_1", "section_1", "section_2"],
        "bnf.paragraph": ["paragraph_1", "paragraph_1", "paragraph_2"],
    }
)

section_result = eds.tl.screen_grouped_therapy(
    therapy_with_prodcode,
    patients,
    events,
    level="section",
    grouping=grouping,
    level_label_col="section",
    min_total_events=2,
)

paragraph_result = eds.tl.screen_grouped_therapy(
    therapy_with_prodcode,
    patients,
    events,
    level="paragraph",
    grouping=grouping,
    level_label_col="paragraph",
    min_total_events=2,
)
```

The grouped result table always includes the canonical `drug` column. Set
`level_label_col` if you also want a level-specific output column such as
`section`, `paragraph`, or `chapter`.

## When to use the lower-level functions

Use {func}`drugscreenpy.tl.compute_ndd_from_text` when you want to
inspect parsed dosage text directly. Use
{func}`drugscreenpy.tl.prepare_prescriptions_from_therapy` when you want
to inspect or customize prescription preparation before screening. Use
`eds.tl.screen_substance_cohort` when your prescription table already has
`start_date` and `duration`.

## Current scope

This port currently targets the substance-level workflow from `original/`.
Grouped chapter-, section-, and paragraph-level workflows are available through
`eds.tl.screen_grouped_therapy(...)` when a `prodcode`-to-group mapping table is
provided. The current text parser covers common CPRD-style dosage instructions,
but not the full `doseminer` feature set from `drugprepr`.
