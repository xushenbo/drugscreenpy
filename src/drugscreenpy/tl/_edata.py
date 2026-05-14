from __future__ import annotations

from collections.abc import Sequence

import pandas as pd

UNS_KEY = "drugscreenpy"
TABLES_KEY = "tables"
RESULTS_KEY = "results"


def is_ehrdata(value: object) -> bool:
    """Return whether a value is an `ehrdata.EHRData` object."""
    from ehrdata import EHRData

    return isinstance(value, EHRData)


def set_table(edata: object, key: str, frame: pd.DataFrame, *, copy: bool = True) -> object:
    """Store a drug-screening workflow table on an `EHRData` object."""
    _check_edata(edata)
    if not isinstance(frame, pd.DataFrame):
        raise TypeError("frame must be a pandas DataFrame")

    _tables(edata)[key] = frame.copy() if copy else frame
    return edata


def get_table(
    edata: object,
    key: str,
    required_columns: Sequence[str] | None = None,
    *,
    required: bool = True,
    copy: bool = True,
) -> pd.DataFrame | None:
    """Fetch a drug-screening workflow table from an `EHRData` object."""
    _check_edata(edata)
    tables = _existing_tables(edata)
    if key not in tables:
        if required:
            raise KeyError(f"No drugscreenpy table named {key!r} in edata.uns['{UNS_KEY}']['{TABLES_KEY}']")
        return None

    frame = tables[key]
    if not isinstance(frame, pd.DataFrame):
        raise TypeError(f"edata.uns['{UNS_KEY}']['{TABLES_KEY}'][{key!r}] must be a pandas DataFrame")

    if required_columns is not None:
        missing = set(required_columns).difference(frame.columns)
        if missing:
            missing_str = ", ".join(sorted(missing))
            raise KeyError(f"Missing required columns in table {key!r}: {missing_str}")

    return frame.copy() if copy else frame


def list_tables(edata: object) -> list[str]:
    """List drug-screening workflow tables stored on an `EHRData` object."""
    _check_edata(edata)
    return sorted(_existing_tables(edata))


def get_patients(edata: object, *, patient_col: str = "patid", copy: bool = True) -> pd.DataFrame:
    """Return `edata.obs` as a patient table with an explicit patient id column."""
    _check_edata(edata)
    patients = edata.obs.copy() if copy else edata.obs
    patient_col_from_index = patient_col not in patients.columns

    if patient_col_from_index:
        patients = patients.reset_index()
        if patient_col not in patients.columns:
            patients = patients.rename(columns={patients.columns[0]: patient_col})

        numeric_ids = pd.to_numeric(patients[patient_col], errors="coerce")
        if numeric_ids.notna().all():
            patients[patient_col] = numeric_ids

    return patients.reset_index(drop=True)


def store_result(edata: object, key: str, result: pd.DataFrame, *, copy: bool = True) -> pd.DataFrame:
    """Store a drug-screening result table on an `EHRData` object and return it."""
    _check_edata(edata)
    if not isinstance(result, pd.DataFrame):
        raise TypeError("result must be a pandas DataFrame")

    _results(edata)[key] = result.copy() if copy else result
    return result


def list_results(edata: object) -> list[str]:
    """List drug-screening result tables stored on an `EHRData` object."""
    _check_edata(edata)
    return sorted(_existing_results(edata))


def _check_edata(edata: object) -> None:
    if not is_ehrdata(edata):
        raise TypeError("edata must be an ehrdata.EHRData object")


def _namespace(edata: object) -> dict:
    namespace = edata.uns.setdefault(UNS_KEY, {})
    if not isinstance(namespace, dict):
        raise TypeError(f"edata.uns[{UNS_KEY!r}] must be a dictionary")
    return namespace


def _tables(edata: object) -> dict[str, pd.DataFrame]:
    tables = _namespace(edata).setdefault(TABLES_KEY, {})
    if not isinstance(tables, dict):
        raise TypeError(f"edata.uns['{UNS_KEY}']['{TABLES_KEY}'] must be a dictionary")
    return tables


def _results(edata: object) -> dict[str, pd.DataFrame]:
    results = _namespace(edata).setdefault(RESULTS_KEY, {})
    if not isinstance(results, dict):
        raise TypeError(f"edata.uns['{UNS_KEY}']['{RESULTS_KEY}'] must be a dictionary")
    return results


def _existing_tables(edata: object) -> dict:
    namespace = edata.uns.get(UNS_KEY, {})
    if not isinstance(namespace, dict):
        raise TypeError(f"edata.uns[{UNS_KEY!r}] must be a dictionary")
    tables = namespace.get(TABLES_KEY, {})
    if not isinstance(tables, dict):
        raise TypeError(f"edata.uns['{UNS_KEY}']['{TABLES_KEY}'] must be a dictionary")
    return tables


def _existing_results(edata: object) -> dict:
    namespace = edata.uns.get(UNS_KEY, {})
    if not isinstance(namespace, dict):
        raise TypeError(f"edata.uns[{UNS_KEY!r}] must be a dictionary")
    results = namespace.get(RESULTS_KEY, {})
    if not isinstance(results, dict):
        raise TypeError(f"edata.uns['{UNS_KEY}']['{RESULTS_KEY}'] must be a dictionary")
    return results
