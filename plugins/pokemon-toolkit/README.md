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

## Roadmap

- **Phase 2:** pm-pokedex - Pokedex lookup via PokeAPI
- **Phase 3:** pm-team-builder - Team composition analysis and suggestions
