# kanjo-pm-toolkit

Claude Code plugin marketplace for Pokemon battle tools.

## Installation

```bash
claude /install pokemon-toolkit from tommytang0122/kanjo-pm-toolkit
```

## Available Plugins

### pokemon-toolkit

AI-powered Pokemon battle tools. See [plugin README](plugins/pokemon-toolkit/README.md) for details.

#### Skills

| Skill | Description | Status |
|-------|-------------|--------|
| pm-dmg-calculator | Level 50 damage calculator | Available |
| pm-pokedex | Pokedex lookup via PokeAPI | Planned |
| pm-team-builder | Team composition analysis | Planned |

## Structure

```
kanjo-pm-toolkit/
├── .claude-plugin/
│   └── marketplace.json           # Marketplace index
├── plugins/
│   └── pokemon-toolkit/           # Plugin
│       ├── README.md
│       └── skills/
│           └── pm-dmg-calculator/
│               └── SKILL.md
├── README.md
└── LICENSE
```

## Design Principles

1. **User provides pre-calculated modifiers** - The damage calculator does not handle STAB, weather, items, etc. Users calculate the final Power value themselves. This keeps tools simple and flexible.
2. **Progressive enhancement** - Start with pure Skills, add scripts and MCP servers only when needed.
3. **Cross-machine portable** - Installable on any machine with Claude Code via the marketplace mechanism.
