"""
Tests para rock_bands_lab.py
Cubre: carga de CSV, métricas, exportación a JSON y logging.
"""

import csv
import json
import logging
from pathlib import Path

import pytest
from estandar_es.rock_bands_lab import (
    compute_metrics,
    export_to_json,
    load_bands,
    run,
    setup_logging,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def logger() -> logging.Logger:
    """Logger silencioso para los tests (nivel WARNING hacia arriba)."""
    log = logging.getLogger("test_rock_bands_lab")
    log.setLevel(logging.WARNING)
    return log


@pytest.fixture()
def sample_csv(tmp_path: Path) -> Path:
    """CSV mínimo con tres bandas para pruebas unitarias."""
    csv_file = tmp_path / "bands.csv"
    rows = [
        {
            "Band": "The Beatles",
            "Country/Region": "UK",
            "City": "Liverpool",
            "Formed": "1960",
            "Primary Genre": "Rock",
        },
        {
            "Band": "Metallica",
            "Country/Region": "USA",
            "City": "Los Angeles",
            "Formed": "1981",
            "Primary Genre": "Heavy Metal",
        },
        {
            "Band": "AC/DC",
            "Country/Region": "Australia",
            "City": "Sydney",
            "Formed": "1973",
            "Primary Genre": "Hard Rock",
        },
    ]
    with csv_file.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return csv_file


@pytest.fixture()
def csv_with_empty_field(tmp_path: Path) -> Path:
    """CSV con una fila que tiene 'City' vacío."""
    csv_file = tmp_path / "bands_empty.csv"
    csv_file.write_text(
        "Band,Country/Region,City,Formed,Primary Genre\n" "Nirvana,USA,,1987,Grunge\n",
        encoding="utf-8",
    )
    return csv_file


@pytest.fixture()
def csv_with_bad_year(tmp_path: Path) -> Path:
    """CSV con un año de formación no numérico."""
    csv_file = tmp_path / "bands_bad_year.csv"
    csv_file.write_text(
        "Band,Country/Region,City,Formed,Primary Genre\n"
        "Fake Band,UK,London,UNKNOWN,Rock\n",
        encoding="utf-8",
    )
    return csv_file


@pytest.fixture()
def real_csv() -> Path:
    """Ruta al CSV real del proyecto."""
    return Path(__file__).resolve().parents[1] / "rock_bands.csv"


# ---------------------------------------------------------------------------
# setup_logging
# ---------------------------------------------------------------------------


class TestSetupLogging:
    def test_returns_logger(self):
        log = setup_logging()
        assert isinstance(log, logging.Logger)

    def test_logger_name(self):
        log = setup_logging()
        assert log.name == "rock_bands_lab"

    def test_level_respected(self):
        log = setup_logging(logging.ERROR)
        assert log.level == logging.ERROR

    def test_has_handler(self):
        log = setup_logging()
        assert len(log.handlers) >= 1


# ---------------------------------------------------------------------------
# load_bands
# ---------------------------------------------------------------------------


class TestLoadBands:
    def test_returns_list(self, sample_csv, logger):
        result = load_bands(sample_csv, logger)
        assert isinstance(result, list)

    def test_correct_count(self, sample_csv, logger):
        result = load_bands(sample_csv, logger)
        assert len(result) == 3

    def test_band_keys_present(self, sample_csv, logger):
        result = load_bands(sample_csv, logger)
        for band in result:
            assert "Band" in band
            assert "Country/Region" in band
            assert "Primary Genre" in band

    def test_formed_converted_to_int(self, sample_csv, logger):
        result = load_bands(sample_csv, logger)
        for band in result:
            assert isinstance(band["Formed"], int)

    def test_file_not_found_raises(self, tmp_path, logger):
        with pytest.raises(FileNotFoundError):
            load_bands(tmp_path / "nonexistent.csv", logger)

    def test_missing_column_raises(self, tmp_path, logger):
        bad_csv = tmp_path / "bad.csv"
        bad_csv.write_text("Band,City\nNirvana,Seattle\n", encoding="utf-8")
        with pytest.raises(ValueError):
            load_bands(bad_csv, logger)

    def test_empty_field_logs_warning(self, csv_with_empty_field, caplog):
        log = setup_logging(logging.DEBUG)
        with caplog.at_level(logging.WARNING, logger="rock_bands_lab"):
            load_bands(csv_with_empty_field, log)
        assert any("campos vacíos" in r.message for r in caplog.records)

    def test_bad_year_becomes_none(self, csv_with_bad_year, logger):
        result = load_bands(csv_with_bad_year, logger)
        assert result[0]["Formed"] is None

    def test_bad_year_logs_warning(self, csv_with_bad_year, caplog):
        log = setup_logging(logging.DEBUG)
        with caplog.at_level(logging.WARNING, logger="rock_bands_lab"):
            load_bands(csv_with_bad_year, log)
        assert any("Formed" in r.message for r in caplog.records)


# ---------------------------------------------------------------------------
# compute_metrics
# ---------------------------------------------------------------------------


class TestComputeMetrics:
    @pytest.fixture()
    def bands(self, sample_csv, logger):
        return load_bands(sample_csv, logger)

    def test_total_bands(self, bands, logger):
        metrics = compute_metrics(bands, logger)
        assert metrics["total_bands"] == 3

    def test_average_year(self, bands, logger):
        metrics = compute_metrics(bands, logger)
        expected = round((1960 + 1981 + 1973) / 3, 1)
        assert metrics["average_formation_year"] == expected

    def test_bands_by_country_keys(self, bands, logger):
        metrics = compute_metrics(bands, logger)
        assert "UK" in metrics["bands_by_country"]
        assert "USA" in metrics["bands_by_country"]
        assert "Australia" in metrics["bands_by_country"]

    def test_bands_by_country_counts(self, bands, logger):
        metrics = compute_metrics(bands, logger)
        assert metrics["bands_by_country"]["UK"] == 1
        assert metrics["bands_by_country"]["USA"] == 1

    def test_bands_by_genre(self, bands, logger):
        metrics = compute_metrics(bands, logger)
        assert "Rock" in metrics["bands_by_genre"]
        assert "Heavy Metal" in metrics["bands_by_genre"]

    def test_bands_by_decade(self, bands, logger):
        metrics = compute_metrics(bands, logger)
        assert "1960s" in metrics["bands_by_decade"]
        assert "1970s" in metrics["bands_by_decade"]
        assert "1980s" in metrics["bands_by_decade"]

    def test_decade_counts(self, bands, logger):
        metrics = compute_metrics(bands, logger)
        assert metrics["bands_by_decade"]["1960s"] == 1
        assert metrics["bands_by_decade"]["1980s"] == 1

    def test_none_year_excluded_from_average(self, logger):
        bands = [
            {
                "Band": "A",
                "Country/Region": "UK",
                "Primary Genre": "Rock",
                "Formed": 2000,
            },
            {
                "Band": "B",
                "Country/Region": "USA",
                "Primary Genre": "Metal",
                "Formed": None,
            },
        ]
        metrics = compute_metrics(bands, logger)
        assert metrics["average_formation_year"] == 2000.0

    def test_all_none_years_average_is_none(self, logger):
        bands = [
            {
                "Band": "X",
                "Country/Region": "UK",
                "Primary Genre": "Rock",
                "Formed": None,
            }
        ]
        metrics = compute_metrics(bands, logger)
        assert metrics["average_formation_year"] is None

    def test_sorted_by_count_descending(self, logger):
        bands = [
            {
                "Band": "A",
                "Country/Region": "UK",
                "Primary Genre": "Rock",
                "Formed": 1970,
            },
            {
                "Band": "B",
                "Country/Region": "UK",
                "Primary Genre": "Rock",
                "Formed": 1975,
            },
            {
                "Band": "C",
                "Country/Region": "USA",
                "Primary Genre": "Rock",
                "Formed": 1980,
            },
        ]
        metrics = compute_metrics(bands, logger)
        countries = list(metrics["bands_by_country"].keys())
        assert countries[0] == "UK"


# ---------------------------------------------------------------------------
# export_to_json
# ---------------------------------------------------------------------------


class TestExportToJson:
    def test_file_is_created(self, tmp_path, logger):
        out = tmp_path / "out" / "result.json"
        export_to_json({"key": "value"}, out, logger)
        assert out.exists()

    def test_creates_parent_dirs(self, tmp_path, logger):
        out = tmp_path / "a" / "b" / "c" / "result.json"
        export_to_json({"x": 1}, out, logger)
        assert out.exists()

    def test_content_is_valid_json(self, tmp_path, logger):
        data = {"total_bands": 30, "bands_by_country": {"UK": 10}}
        out = tmp_path / "result.json"
        export_to_json(data, out, logger)
        loaded = json.loads(out.read_text(encoding="utf-8"))
        assert loaded == data

    def test_unicode_preserved(self, tmp_path, logger):
        data = {"ciudad": "México", "banda": "Café Tacvba"}
        out = tmp_path / "unicode.json"
        export_to_json(data, out, logger)
        content = out.read_text(encoding="utf-8")
        assert "México" in content
        assert "Café Tacvba" in content

    def test_uses_indentation(self, tmp_path, logger):
        out = tmp_path / "pretty.json"
        export_to_json({"a": 1}, out, logger)
        content = out.read_text(encoding="utf-8")
        assert "\n" in content


# ---------------------------------------------------------------------------
# run (integración con CSV real)
# ---------------------------------------------------------------------------


class TestRun:
    def test_run_returns_dict(self, real_csv, tmp_path, logger):
        out = tmp_path / "metrics.json"
        result = run(real_csv, out, logger)
        assert isinstance(result, dict)

    def test_run_total_bands(self, real_csv, tmp_path, logger):
        out = tmp_path / "metrics.json"
        result = run(real_csv, out, logger)
        assert result["total_bands"] == 30

    def test_run_creates_json_file(self, real_csv, tmp_path, logger):
        out = tmp_path / "metrics.json"
        run(real_csv, out, logger)
        assert out.exists()

    def test_run_json_has_expected_keys(self, real_csv, tmp_path, logger):
        out = tmp_path / "metrics.json"
        run(real_csv, out, logger)
        data = json.loads(out.read_text(encoding="utf-8"))
        for key in (
            "total_bands",
            "average_formation_year",
            "bands_by_country",
            "bands_by_genre",
            "bands_by_decade",
        ):
            assert key in data

    def test_run_uk_has_most_bands(self, real_csv, tmp_path, logger):
        out = tmp_path / "metrics.json"
        result = run(real_csv, out, logger)
        first_country = next(iter(result["bands_by_country"]))
        assert first_country == "UK"

    def test_run_creates_logger_if_none(self, real_csv, tmp_path):
        out = tmp_path / "metrics.json"
        result = run(real_csv, out, logger=None)
        assert "total_bands" in result
