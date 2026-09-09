"""Unit tests for WasherModelLookup engine."""

import pytest
from ifb_washer_models import WasherModelLookup, ApplianceArchetype


@pytest.fixture
def lookup():
    return WasherModelLookup()


def test_lookup_all_models(lookup):
    models = lookup.all_models
    assert len(models) == 247
    assert all(m.model_name for m in models)
    assert all(m.manual_code for m in models)
    assert all(m.capacity_kg > 0 for m in models)
    assert all(m.spin_max_rpm > 0 for m in models)


def test_lookup_all_manuals(lookup):
    manuals = lookup.all_manuals
    assert len(manuals) == 23
    assert all(m.manual_code for m in manuals)
    assert all(m.archetype for m in manuals)


def test_lookup_exact_model(lookup):
    # Executive Plus ZXS WD 8.5/6.5
    model = lookup.get_model_info("Executive Plus ZXS WD 8.5/6.5")
    assert model is not None
    assert model.series == "Executive Plus"
    assert model.capacity_kg == 8.5
    assert model.spin_max_rpm == 1400
    assert model.manual_code == "MAN_742_E"
    assert model.archetype == ApplianceArchetype.WASHER_DRYER_REFRESHER


def test_lookup_fuzzy_normalized_model(lookup):
    # Case insensitivity, IFB prefix stripping
    model = lookup.get_model_info("IFB executive plus zxs wd 8.5/6.5")
    assert model is not None
    assert model.manual_code == "MAN_742_E"

    # Senator Touch model
    model_touch = lookup.get_model_info("Senator GXN 8012")
    assert model_touch is not None
    assert model_touch.archetype == ApplianceArchetype.FRONT_LOAD_TOUCH_STEPPER


def test_lookup_manual_info(lookup):
    manual = lookup.get_manual_info("MAN_742_E")
    assert manual is not None
    assert manual.file_name == "Washer_Dryer_742_E.pdf"
    assert manual.archetype == ApplianceArchetype.WASHER_DRYER_REFRESHER
    assert manual.panel_page == 4


def test_lookup_dial_programs(lookup):
    # 742 Washer Dryer dial (14 detents)
    dial = lookup.get_dial_programs("MAN_742_E")
    assert len(dial) == 14
    assert dial[1] == "Wash + Dry 2Hr"
    assert dial[2] == "Wash + Dry 4Hr"
    assert dial[4] == "Refresh"
    assert dial[6] == "CradleWash®"
    assert dial[7] == "Wool"
    assert dial[12] == "Cotton"
    assert dial[13] == "Mix / Daily"
    assert dial[14] == "Express 15'"
