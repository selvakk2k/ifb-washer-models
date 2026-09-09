"""Export SQLite reference database to validated JSON files."""

import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "ifb_washer_models" / "data" / "ifb_smart_manuals.db"
OUTPUT_DIR = Path(__file__).parent.parent / "ifb_washer_models" / "data"
ROOT_DIR = Path(__file__).parent.parent


def export_all():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # 1. Manuals
    manuals = [dict(row) for row in cur.execute("SELECT * FROM manuals ORDER BY id").fetchall()]
    with open(OUTPUT_DIR / "manuals.json", "w", encoding="utf-8") as f:
        json.dump(manuals, f, indent=2)

    # 2. Models
    models = [dict(row) for row in cur.execute("SELECT * FROM models ORDER BY id").fetchall()]
    with open(OUTPUT_DIR / "models.json", "w", encoding="utf-8") as f:
        json.dump(models, f, indent=2)
    # Also write to root models.json
    with open(ROOT_DIR / "models.json", "w", encoding="utf-8") as f:
        json.dump(models, f, indent=2)

    # 3. Programs
    programs = [dict(row) for row in cur.execute("SELECT * FROM programs ORDER BY id").fetchall()]
    with open(OUTPUT_DIR / "programs.json", "w", encoding="utf-8") as f:
        json.dump(programs, f, indent=2)

    # 4. Program Gating
    raw_gating = [dict(row) for row in cur.execute("SELECT * FROM program_gating ORDER BY id").fetchall()]
    gating = []
    for g in raw_gating:
        item = dict(g)
        # Parse nested JSON fields
        for field in ["allowed_temps", "allowed_spins", "allowed_dry_modes"]:
            if item.get(field) and isinstance(item[field], str):
                try:
                    item[field] = json.loads(item[field])
                except json.JSONDecodeError:
                    pass
        gating.append(item)

    with open(OUTPUT_DIR / "program_gating.json", "w", encoding="utf-8") as f:
        json.dump(gating, f, indent=2)
    with open(ROOT_DIR / "program_gating.json", "w", encoding="utf-8") as f:
        json.dump(gating, f, indent=2)

    # 5. Fascia labels & special features & aliases
    fascia = [dict(row) for row in cur.execute("SELECT * FROM fascia_labels ORDER BY id").fetchall()]
    with open(OUTPUT_DIR / "fascia_labels.json", "w", encoding="utf-8") as f:
        json.dump(fascia, f, indent=2)

    special = [dict(row) for row in cur.execute("SELECT * FROM special_features ORDER BY id").fetchall()]
    with open(OUTPUT_DIR / "special_features.json", "w", encoding="utf-8") as f:
        json.dump(special, f, indent=2)

    aliases = [dict(row) for row in cur.execute("SELECT * FROM aliases ORDER BY id").fetchall()]
    with open(OUTPUT_DIR / "aliases.json", "w", encoding="utf-8") as f:
        json.dump(aliases, f, indent=2)

    # 6. Archetypes summary
    archetypes = {
        "Washer-Dryer Refresher": {
            "description": "14-Detent Dual-Arc Mechanical Rotary Knob + Capacitive Touch Options Panel",
            "physical_detents": 14,
            "has_my_ifb_gateway": False,
            "supports_drying": True,
            "supports_steam": True,
            "tub_clean_trigger": "Hold Time Saver for 3s (Packet Code 15)",
            "detent_arcs": {
                "right_arc": [1, 2, 3, 4, 5, 6, 7],
                "left_arc": [8, 9, 10, 11, 12, 13, 14],
            },
        },
        "Front Load Smart Rotary": {
            "description": "9-Detent Rotary Selector + Position 10 'My IFB' Smartphone App Gateway",
            "physical_detents": 9,
            "has_my_ifb_gateway": True,
            "gateway_slot": 10,
            "supports_drying": False,
            "supports_steam": True,
            "tub_clean_trigger": "Hold Options for 3s / Dial Detent 15",
        },
        "Front Load Touch/Stepper": {
            "description": "Full Glass Touch Fascia with Sequential 11-Cycle LED Step Ladder",
            "physical_detents": 0,
            "has_my_ifb_gateway": False,
            "supports_drying": False,
            "supports_steam": True,
            "tub_clean_trigger": "Step to Tub Clean / Dedicated Button",
        },
        "Top Load Smart Wi-Fi": {
            "description": "Tactile Push Buttons + Vertical 10/11-Cycle LED Program Ladder",
            "physical_detents": 0,
            "has_my_ifb_gateway": False,
            "supports_drying": False,
            "supports_air_dry": True,
            "supports_water_levels": True,
            "water_levels": 10,
            "tub_clean_trigger": "Dedicated PreClean / Tub Clean Button",
        },
    }
    with open(OUTPUT_DIR / "archetypes.json", "w", encoding="utf-8") as f:
        json.dump(archetypes, f, indent=2)
    with open(ROOT_DIR / "archetypes.json", "w", encoding="utf-8") as f:
        json.dump(archetypes, f, indent=2)

    print(f"Export completed: {len(models)} models, {len(manuals)} manuals, {len(programs)} programs, {len(gating)} gating rules.")


if __name__ == "__main__":
    export_all()
