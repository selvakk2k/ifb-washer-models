# IFB Washer Hardware Profiles & Wash Guide (`ifb-washer-models`)

[![Version](https://img.shields.io/github/v/release/selvakk2k/ifb-washer-models?style=flat-square)](https://github.com/selvakk2k/ifb-washer-models/releases)
[![AI-Assisted](https://img.shields.io/badge/AI%20Assisted-Antigravity%20%7C%20Claude-blueviolet?style=flat-square&logo=google)](https://github.com/selvakk2k)
[![AI Attribution](https://img.shields.io/badge/AI%20Attribution-AIA%20PAI%20Nc%20Hin-orange?style=flat-square)](https://aiattribution.github.io/interpret-attribution)

> [!NOTE]
> **Regional Scope**: This database tracks IFB smart washing machines and washer-dryers sold in the **Indian Market** (Wi-Fi enabled and front/top load models).

A unified hardware capability database, model lookup engine, and wash guide reference for IFB smart washing machines and washer-dryers. Covers **247 commercial models**, **23 factory user manuals**, **349 wash programs**, and **263 capability gating rules**, providing verified hardware operational limits for Home Assistant integrations and custom cards.

---

## Table of Contents
* [Installation](#installation)
* [Model Capability Database & Lookup Engine](#model-capability-database--lookup-engine)
  * [Python Backend Usage](#python-backend-usage)
  * [Offline Bundled Data](#offline-bundled-data)
* [The Four Hardware Archetypes](#the-four-hardware-archetypes)
* [Hardware Capability Gating Rules](#hardware-capability-gating-rules)
* [Database Summary](#database-summary)
* [My Python Libraries](#my-python-libraries)
* [Credits & License](#credits--license)

---

## Installation

Install the Python package via `pip`:

```bash
pip install ifb-washer-models
```

---

## Model Capability Database & Lookup Engine

### Python Backend Usage

Query model metadata, detent mappings, and program capability limits using the normalized lookup engine:

```python
from ifb_washer_models import WasherModelLookup

lookup = WasherModelLookup()

# 1. Resolve commercial model names (handles spaces, hyphens, and casing automatically)
model = lookup.get_model_info("Executive Plus ZXS WD 8.5/6.5")

print(f"Series:      {model.series}")
print(f"Capacity:    {model.capacity_kg} kg")
print(f"Max Spin:    {model.spin_max_rpm} RPM")
print(f"Manual Code: {model.manual_code}")
print(f"Archetype:   {model.archetype}")

# 2. Get physical rotary selector switch detent mappings (1..14)
dial_map = lookup.get_dial_programs(model.manual_code)
print("Physical Detents:", dial_map)
# => {1: 'Wash + Dry 2Hr', 2: 'Wash + Dry 4Hr', 4: 'Refresh', 6: 'CradleWash®', 12: 'Cotton', ...}

# 3. Query program capability gating (temperatures, spin speeds, drying modes, modifiers)
caps = lookup.get_program_capabilities(model.manual_code, "CradleWash®")

print("Allowed Temps: ", caps.allowed_temps)     # ('Cold', '30°C', '40°C')
print("Allowed Spins: ", caps.allowed_spins)     # ('No Spin', '400 RPM', '600 RPM')
print("Supports Dry:  ", caps.supports_dry)      # True
print("Dry Modes:     ", caps.allowed_dry_modes) # ('No Dry', 'Gentle Dry', '30 Minutes', '1 Hour')
print("Supports Steam:", caps.supports_steam)    # False
```

### Offline Bundled Data

The package embeds all database tables in JSON format (`models.json`, `manuals.json`, `program_gating.json`, `programs.json`, `archetypes.json`) under `ifb_washer_models/data/`. Applications can import or read these files directly with zero external network calls.

---

## The Four Hardware Archetypes

IFB manufactures its smart Wi-Fi appliances across 4 distinct physical control archetypes:

| Archetype | Control Interface | Physical Detents | App Gateway Mode | Drying Support | Example Series |
|---|---|:---:|:---:|:---:|---|
| **Washer-Dryer Refresher** | 14-Detent Dual-Arc Rotary + Touch Panel | 14 | None (Fixed Detents) | ✅ Full Heated Dry | Executive ZXS, Senator VX (742 / 772 / 850) |
| **Front Load Smart Rotary** | 9-Detent Rotary + "My IFB" Gateway Slot | 9 | Position 10 ("My IFB") | ❌ No | Senator Plus, Elena, Serenade (653 / 752 / 790) |
| **Front Load Touch/Stepper**| Capacitive Touch Fascia (11-LED Step Ladder) | 0 | None (Touch Stepper) | ❌ No | Senator Touch, Executive Touch (780 / 800) |
| **Top Load Smart Wi-Fi** | Push Buttons + Vertical 10-LED Program Ladder | 0 | None (LED Ladder) | ⚠️ Unheated Air Dry | TL_013 .. TL_360 Series |

---

## Hardware Capability Gating Rules

The database enforces physical MCU limits derived from official factory manuals to prevent sending incompatible command combinations:

| Program | Limits on Washer-Dryer (`MAN_742_E`) | Limits on Front Load Smart (`MAN_752_I`) | Limits on Front Load Touch (`MAN_780_E`) |
|---|---|---|---|
| **Cotton** | Max 60°C • Max 1200 RPM • Dry supported | Max 95°C • Max 1400 RPM • No Dry | Max 95°C • Max 1400 RPM • No Dry |
| **Baby Wear** | Max 60°C • Max 1000 RPM • Dry supported | Max 60°C • Max 800 RPM • No Dry | Max 60°C • Max 800 RPM • No Dry |
| **CradleWash®** | Max 40°C • Max 600 RPM • Gentle/Timed Dry | Max 40°C • Max 600 RPM • No Dry | Max 40°C • Max 600 RPM • No Dry |
| **Refresh** | Cold / 50°C • No Spin • Steam • No Dry | N/A (Washer-Dryer exclusive) | N/A (Washer-Dryer exclusive) |
| **Express 15'** | Max 40°C • Up to 2h Dry | Max 40°C • No Dry | Max 30°C • No Dry |

---

## Database Summary

- **Commercial Models**: 247 models across Executive, Senator, Elena, Serenade, and Top Load series.
- **Factory User Manuals**: 23 audited manual families.
- **Wash Cycles**: 349 individual program entries.
- **Gating Rules**: 263 cycle-to-modifier constraint records.
- **Primary Data Sources**: Official IFB factory user manuals, firmware MCU frame dumps, and empirical local GainSpan telemetry captures.

---

## My Python Libraries

| Library | PyPI Package | Description | Status |
| :--- | :--- | :--- | :--- |
| [Panasonic AC Models](https://github.com/selvakk2k/panasonic-ac-models) | `panasonic-ac-models` | Hardware profiles, capability lookup & IR protocol generator for Indian Panasonic ACs | `Stable` |
| [IFB Washer Models](https://github.com/selvakk2k/ifb-washer-models) | `ifb-washer-models` | Unified hardware database, model lookup & cycle capability gating for IFB smart washers | `Stable` |
| [MirAIe AC API Client](https://github.com/selvakk2k/miraie-ac-in) | `miraie-ac-in` | Async MQTT & REST API client for Panasonic MirAIe-connected Air Conditioners | `Stable` |

---

## Credits & License

### Project Contributors & AI Attribution
* **Lead Architecture & Hardware Validation**: [@selvakk2k](https://github.com/selvakk2k) — physical appliance reverse engineering, manual audits, and hardware validation.
* **Code Implementation & Engineering**: **Antigravity** (Google DeepMind) — database schema design, normalized lookup engine, automated tests, and export pipelines.
* **Pre-Release Code Review & Auditing**: **Claude** (Anthropic) — data referential integrity audits and capability rule verification.

Licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
