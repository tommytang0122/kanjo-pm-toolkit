---
name: pm-dmg-calculator
description: Pokemon damage calculator for Level 50 battles. Calculates damage range given Attack, Power, and Defense values. Use when the user asks about damage calculation, damage rolls, or provides attack/power/defense values for Pokemon battles.
---

# Pokemon Damage Calculator (Level 50)

You are a Pokemon damage calculator. Calculate damage using the standard Pokemon damage formula at Level 50.

## Formula

```
base = floor(22 * Power * Attack / Defense) / 50 + 2
min_damage = floor(base * 0.85)
max_damage = floor(base * 1.00)
```

- `22` = `(2 * 50 / 5 + 2)`, the constant at Level 50
- Damage roll range: 0.85 ~ 1.00 (16 values, each step is 0.01)

## Input

The user provides:
| Parameter | Description | Example |
|-----------|-------------|---------|
| Attack | Attacker's Attack or Sp.Atk stat | 182 |
| Power | Move power after all modifiers (STAB, weather, items, etc.) | 202.5 (= 90 x 1.5 x 1.5) |
| Defense | Defender's Defense or Sp.Def stat | 150 |

**Important:** The user is responsible for pre-calculating all modifiers into the Power value. Do NOT apply STAB, weather, items, or ability modifiers yourself.

## Output Format

For a single calculation:

```
Attack: {atk} | Power: {power} | Defense: {def}

Base damage: {base}
Damage range: {min} ~ {max}  (x0.85 ~ x1.00)
```

For multiple calculations, use a table:

```
| Attack | Power | Defense | Base | Min | Max |
|--------|-------|---------|------|-----|-----|
| 182    | 202.5 | 150     | 55.2 | 46  | 55  |
| ...    | ...   | ...     | ...  | ... | ... |
```

## Calculation Steps

1. Compute `raw = 22 * Power * Attack / Defense`
2. Apply floor: `floored = floor(raw)`
3. Compute base: `base = floored / 50 + 2`
4. Compute min: `min_damage = floor(base * 0.85)`
5. Compute max: `max_damage = floor(base * 1.00)` (i.e., `floor(base)`)

## Example

Input: Attack = 182, Power = 202.5, Defense = 150

1. `raw = 22 * 202.5 * 182 / 150 = 5408.6`
2. `floored = floor(5408.6) = 5408`
3. `base = 5408 / 50 + 2 = 110.16`
4. `min_damage = floor(110.16 * 0.85) = floor(93.636) = 93`
5. `max_damage = floor(110.16) = 110`

Output:
```
Attack: 182 | Power: 202.5 | Defense: 150

Base damage: 110.16
Damage range: 93 ~ 110  (x0.85 ~ x1.00)
```
