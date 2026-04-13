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


def main():
    pass


if __name__ == "__main__":
    main()
