"""Test cross-table referential integrity and valid JSON structures."""

import json
from pathlib import Path
import pytest

DATA_DIR = Path(__file__).parent.parent / "ifb_washer_models" / "data"


def test_models_json_validity():
    with open(DATA_DIR / "models.json", "r", encoding="utf-8") as f:
        models = json.load(f)
    assert len(models) == 247

    with open(DATA_DIR / "manuals.json", "r", encoding="utf-8") as f:
        manuals = {m["manual_code"] for m in json.load(f)}

    # Verify all models reference a valid manual code
    for m in models:
        assert m["manual_code"] in manuals, f"Model {m['model_name']} references unknown manual {m['manual_code']}"


def test_program_gating_json_validity():
    with open(DATA_DIR / "program_gating.json", "r", encoding="utf-8") as f:
        gating = json.load(f)
    assert len(gating) == 263

    with open(DATA_DIR / "manuals.json", "r", encoding="utf-8") as f:
        manuals = {m["manual_code"] for m in json.load(f)}

    for g in gating:
        assert g["manual_code"] in manuals
        assert isinstance(g["allowed_temps"], list)
        assert isinstance(g["allowed_spins"], list)
        assert isinstance(g["allowed_dry_modes"], list)


def test_archetypes_json_validity():
    with open(DATA_DIR / "archetypes.json", "r", encoding="utf-8") as f:
        archetypes = json.load(f)
    assert "Washer-Dryer Refresher" in archetypes
    assert "Front Load Smart Rotary" in archetypes
    assert "Front Load Touch/Stepper" in archetypes
    assert "Top Load Smart Wi-Fi" in archetypes
