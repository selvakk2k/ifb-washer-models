"""Unit tests for capability gating and wash guide limits."""

import pytest
from ifb_washer_models import WasherModelLookup


@pytest.fixture
def lookup():
    return WasherModelLookup()


def test_gating_washer_dryer_refresh(lookup):
    caps = lookup.get_program_capabilities("MAN_742_E", "Refresh")
    assert caps is not None
    assert "Cold" in caps.allowed_temps
    assert "50°C" in caps.allowed_temps
    assert caps.allowed_spins == ("No Spin",)
    assert caps.supports_dry is False
    assert caps.supports_steam is True


def test_gating_washer_dryer_cradlewash(lookup):
    caps = lookup.get_program_capabilities("MAN_742_E", "CradleWash®")
    assert caps is not None
    assert "95°C" not in caps.allowed_temps
    assert "Cold" in caps.allowed_temps
    assert "30°C" in caps.allowed_temps
    assert "40°C" in caps.allowed_temps
    assert caps.supports_dry is True
    assert "Gentle Dry" in caps.allowed_dry_modes or "30 Minutes" in caps.allowed_dry_modes


def test_gating_washer_dryer_cotton(lookup):
    caps = lookup.get_program_capabilities("MAN_742_E", "Cotton")
    assert caps is not None
    assert caps.supports_dry is True
    assert caps.supports_prewash is True
    assert caps.supports_time_saver is True
    assert "Cupboard Dry" in caps.allowed_dry_modes
    assert "1400 RPM" in caps.allowed_spins or "1200 RPM" in caps.allowed_spins


def test_gating_front_load_smart_rotary_baby_wear(lookup):
    # Front Load Smart Rotary manual MAN_752_I
    caps = lookup.get_program_capabilities("MAN_752_I", "Baby Wear")
    assert caps is not None
    assert caps.supports_dry is False
    # Baby Wear on front loader has 800 RPM max limit
    assert "1400 RPM" not in caps.allowed_spins
    assert "800 RPM" in caps.allowed_spins


def test_gating_dict_conversion(lookup):
    caps = lookup.get_program_capabilities("MAN_742_E", "Mix / Daily")
    assert caps is not None
    d = caps.to_dict()
    assert isinstance(d, dict)
    assert d["program_name"] == "Mix / Daily"
    assert isinstance(d["allowed_temps"], list)
    assert isinstance(d["allowed_spins"], list)
    assert isinstance(d["allowed_dry_modes"], list)
