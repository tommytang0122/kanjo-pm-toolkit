---
name: pm-pokedex-update
description: Update the local Pokedex database by fetching all Pokemon data from PokeAPI. Use when the user wants to update or rebuild the Pokemon database.
---

# Pokedex Update

Fetch all Pokemon data from PokeAPI and write to local `.md` files.

## Usage

Run the update script:

```bash
cd plugins/pokemon-toolkit
pip install requests tqdm
python scripts/update_pokedex.py
```

## What It Does

1. Fetches all Pokemon species from PokeAPI (including all forms: Mega, regional, etc.)
2. Writes `data/index.md` — compact index for search/filter
3. Writes `data/pokemon/{id}.md` — full details per Pokemon

## Notes

- First run fetches ~1025 species with ~3000-5000 API requests. Takes several minutes.
- Concurrent requests (max 20) with progress bar.
- Failed fetches are logged to `data/errors.log` without stopping the process.
