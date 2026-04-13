"""Fetch all Pokemon data from PokeAPI and write local .md files."""

import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None


POKEAPI_BASE = "https://pokeapi.co/api/v2"
MAX_WORKERS = 20
DATA_DIR = Path(__file__).parent.parent / "data"
POKEMON_DIR = DATA_DIR / "pokemon"


STAT_MAP = {
    "hp": "hp", "attack": "atk", "defense": "def",
    "special-attack": "spa", "special-defense": "spd", "speed": "spe",
}

GEN_MAP = {
    "generation-i": 1, "generation-ii": 2, "generation-iii": 3,
    "generation-iv": 4, "generation-v": 5, "generation-vi": 6,
    "generation-vii": 7, "generation-viii": 8, "generation-ix": 9,
}


def _parse_pokemon_response(data):
    """Parse a /pokemon/{id} response into compact form."""
    types = [t["type"]["name"].capitalize() for t in sorted(data["types"], key=lambda t: t["slot"])]
    stats = {STAT_MAP[s["stat"]["name"]]: s["base_stat"] for s in data["stats"]}
    abilities = []
    for a in sorted(data["abilities"], key=lambda a: a["slot"]):
        name = a["ability"]["name"].replace("-", " ").title()
        if a["is_hidden"]:
            name += " (H)"
        abilities.append(name)
    moves = []
    for m in data["moves"]:
        move_name = m["move"]["name"].replace("-", " ").title()
        details = m["version_group_details"]
        if not details:
            continue
        latest = details[-1]
        method = latest["move_learn_method"]["name"]
        level = latest["level_learned_at"]
        if method == "level-up" and level > 0:
            moves.append({"name": move_name, "method": f"lv{level}"})
        elif method == "machine":
            moves.append({"name": move_name, "method": "TM"})
        elif method == "egg":
            moves.append({"name": move_name, "method": "egg"})
        elif method == "tutor":
            moves.append({"name": move_name, "method": "tutor"})
        else:
            moves.append({"name": move_name, "method": method})
    return {"types": types, "stats": stats, "abilities": abilities, "moves": moves}


def fetch_pokemon_data(species_url):
    """Fetch and parse all data for one Pokemon species."""
    species_resp = requests.get(species_url, timeout=30)
    species_resp.raise_for_status()
    species = species_resp.json()

    species_id = species["id"]
    names = {entry["language"]["name"]: entry["name"] for entry in species["names"]}
    generation = GEN_MAP.get(species["generation"]["name"], 0)

    # Determine species base name from the default variety's pokemon name
    species_base_name = next(
        (v["pokemon"]["name"] for v in species["varieties"] if v["is_default"]),
        species.get("name", "")
    )

    forms = []
    for variety in species["varieties"]:
        pokemon_url = variety["pokemon"]["url"]
        pokemon_resp = requests.get(pokemon_url, timeout=30)
        pokemon_resp.raise_for_status()
        pokemon = pokemon_resp.json()
        parsed = _parse_pokemon_response(pokemon)

        form_name = variety["pokemon"]["name"]
        if variety["is_default"]:
            form_name = "base"
        else:
            form_name = form_name.replace(f"{species_base_name}-", "")

        forms.append({
            "name": form_name,
            "types": parsed["types"],
            "stats": parsed["stats"],
            "abilities": parsed["abilities"],
            "moves": parsed["moves"],
        })

    base = forms[0] if forms else {}
    return {
        "id": species_id,
        "names": names,
        "generation": generation,
        "types": base.get("types", []),
        "stats": base.get("stats", {}),
        "abilities": base.get("abilities", []),
        "forms": forms,
    }


def fetch_species_list():
    """Fetch the full list of Pokemon species from PokeAPI."""
    resp = requests.get(f"{POKEAPI_BASE}/pokemon-species?limit=10000", timeout=30)
    resp.raise_for_status()
    return resp.json()["results"]


def main():
    pass


if __name__ == "__main__":
    main()
