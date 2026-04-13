# Pokemon Toolkit

AI-powered Pokemon battle tools for Claude Code.

## Skills

### pm-dmg-calculator

Pokemon damage calculator for Level 50 battles. Calculates damage range given Attack, Power, and Defense values.

**Usage:** `/pm-dmg-calculator` or mention damage calculation in conversation.

**Input:**
| Parameter | Description | Example |
|-----------|-------------|---------|
| Attack | Attacker's Attack or Sp.Atk stat | 182 |
| Power | Move power after all modifiers | 202.5 |
| Defense | Defender's Defense or Sp.Def stat | 150 |

**Note:** You are responsible for pre-calculating all modifiers (STAB, weather, items, abilities) into the Power value.

**Example output:**
```
Attack: 182 | Power: 202.5 | Defense: 150

Base damage: 110.16
Damage range: 93 ~ 110  (x0.85 ~ x1.00)
```

### pm-pokedex-update

Update the local Pokedex database by fetching all Pokemon data from PokeAPI.

**Usage:** `/pm-pokedex-update`

**What it does:**
1. Fetches all ~1025 Pokemon species from PokeAPI (including Mega, regional forms)
2. Writes `data/index.md` — compact index for search/filter
3. Writes `data/pokemon/{id}.md` — full details per Pokemon

**Requirements:** Python 3, `requests`, `tqdm` (optional)

**Note:** First run makes ~3000-5000 API requests and takes several minutes.

## Roadmap

- **pm-dmg-planner:** Battle damage scenario planner (Lv.50 Doubles)
- **pm-team-builder:** Team composition analysis and suggestions
