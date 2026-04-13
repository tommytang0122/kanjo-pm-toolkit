"""Tests for update_pokedex.py parsing and formatting logic."""

from unittest.mock import patch, Mock
from update_pokedex import fetch_species_list


def test_placeholder():
    assert True


def test_fetch_species_list():
    mock_response = Mock()
    mock_response.json.return_value = {
        "count": 3,
        "results": [
            {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon-species/1/"},
            {"name": "ivysaur", "url": "https://pokeapi.co/api/v2/pokemon-species/2/"},
            {"name": "venusaur", "url": "https://pokeapi.co/api/v2/pokemon-species/3/"},
        ]
    }
    mock_response.raise_for_status = Mock()

    with patch("update_pokedex.requests.get", return_value=mock_response) as mock_get:
        result = fetch_species_list()
        mock_get.assert_called_once_with(
            "https://pokeapi.co/api/v2/pokemon-species?limit=10000",
            timeout=30,
        )
        assert result == [
            {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon-species/1/"},
            {"name": "ivysaur", "url": "https://pokeapi.co/api/v2/pokemon-species/2/"},
            {"name": "venusaur", "url": "https://pokeapi.co/api/v2/pokemon-species/3/"},
        ]


from update_pokedex import fetch_pokemon_data


MOCK_SPECIES_RESPONSE = {
    "id": 6,
    "names": [
        {"language": {"name": "en"}, "name": "Charizard"},
        {"language": {"name": "ja-Hrkt"}, "name": "リザードン"},
        {"language": {"name": "zh-Hant"}, "name": "噴火龍"},
    ],
    "generation": {"name": "generation-i"},
    "varieties": [
        {"is_default": True, "pokemon": {"name": "charizard", "url": "https://pokeapi.co/api/v2/pokemon/6/"}},
        {"is_default": False, "pokemon": {"name": "charizard-mega-x", "url": "https://pokeapi.co/api/v2/pokemon/10034/"}},
    ]
}

MOCK_POKEMON_BASE = {
    "id": 6,
    "types": [
        {"slot": 1, "type": {"name": "fire"}},
        {"slot": 2, "type": {"name": "flying"}},
    ],
    "stats": [
        {"base_stat": 78, "stat": {"name": "hp"}},
        {"base_stat": 84, "stat": {"name": "attack"}},
        {"base_stat": 78, "stat": {"name": "defense"}},
        {"base_stat": 109, "stat": {"name": "special-attack"}},
        {"base_stat": 85, "stat": {"name": "special-defense"}},
        {"base_stat": 100, "stat": {"name": "speed"}},
    ],
    "abilities": [
        {"ability": {"name": "blaze"}, "is_hidden": False, "slot": 1},
        {"ability": {"name": "solar-power"}, "is_hidden": True, "slot": 3},
    ],
    "moves": [
        {
            "move": {"name": "flamethrower"},
            "version_group_details": [
                {"level_learned_at": 46, "move_learn_method": {"name": "level-up"}, "version_group": {"name": "scarlet-violet"}},
            ]
        },
        {
            "move": {"name": "dragon-claw"},
            "version_group_details": [
                {"level_learned_at": 0, "move_learn_method": {"name": "machine"}, "version_group": {"name": "scarlet-violet"}},
            ]
        },
    ]
}

MOCK_POKEMON_MEGA_X = {
    "id": 10034,
    "types": [
        {"slot": 1, "type": {"name": "fire"}},
        {"slot": 2, "type": {"name": "dragon"}},
    ],
    "stats": [
        {"base_stat": 78, "stat": {"name": "hp"}},
        {"base_stat": 130, "stat": {"name": "attack"}},
        {"base_stat": 111, "stat": {"name": "defense"}},
        {"base_stat": 130, "stat": {"name": "special-attack"}},
        {"base_stat": 85, "stat": {"name": "special-defense"}},
        {"base_stat": 100, "stat": {"name": "speed"}},
    ],
    "abilities": [
        {"ability": {"name": "tough-claws"}, "is_hidden": False, "slot": 1},
    ],
    "moves": []
}


def test_fetch_pokemon_data():
    def mock_get(url, timeout=30):
        mock_resp = Mock()
        mock_resp.raise_for_status = Mock()
        if "pokemon-species/6" in url:
            mock_resp.json.return_value = MOCK_SPECIES_RESPONSE
        elif "pokemon/10034" in url:
            mock_resp.json.return_value = MOCK_POKEMON_MEGA_X
        elif "pokemon/6" in url:
            mock_resp.json.return_value = MOCK_POKEMON_BASE
        return mock_resp

    with patch("update_pokedex.requests.get", side_effect=mock_get):
        result = fetch_pokemon_data("https://pokeapi.co/api/v2/pokemon-species/6/")

    assert result["id"] == 6
    assert result["names"]["en"] == "Charizard"
    assert result["names"]["zh-Hant"] == "噴火龍"
    assert result["generation"] == 1
    assert result["types"] == ["Fire", "Flying"]
    assert result["stats"]["atk"] == 84
    assert len(result["forms"]) == 2
    assert result["forms"][1]["name"] == "mega-x"
    assert result["forms"][1]["types"] == ["Fire", "Dragon"]


from update_pokedex import format_pokemon_md


def test_format_pokemon_md_single_form():
    data = {
        "id": 25,
        "names": {"en": "Pikachu", "ja-Hrkt": "ピカチュウ", "zh-Hant": "皮卡丘"},
        "generation": 1,
        "types": ["Electric"],
        "stats": {"hp": 35, "atk": 55, "def": 40, "spa": 50, "spd": 50, "spe": 90},
        "abilities": ["Static", "Lightning Rod (H)"],
        "forms": [
            {
                "name": "base",
                "types": ["Electric"],
                "stats": {"hp": 35, "atk": 55, "def": 40, "spa": 50, "spd": 50, "spe": 90},
                "abilities": ["Static", "Lightning Rod (H)"],
                "moves": [
                    {"name": "Thunder Shock", "method": "lv1"},
                    {"name": "Thunderbolt", "method": "TM"},
                ],
            }
        ],
    }
    result = format_pokemon_md(data)
    assert "#025 Pikachu / ピカチュウ / 皮卡丘" in result
    assert "Type: Electric | Gen: 1" in result
    assert "HP 35 | ATK 55 | DEF 40 | SPA 50 | SPD 50 | SPE 90" in result
    assert "Abilities: Static, Lightning Rod (H)" in result
    assert "Thunder Shock (lv1)" in result
    assert "Thunderbolt (TM)" in result


def test_format_pokemon_md_with_forms():
    data = {
        "id": 6,
        "names": {"en": "Charizard", "ja-Hrkt": "リザードン", "zh-Hant": "噴火龍"},
        "generation": 1,
        "types": ["Fire", "Flying"],
        "stats": {"hp": 78, "atk": 84, "def": 78, "spa": 109, "spd": 85, "spe": 100},
        "abilities": ["Blaze", "Solar Power (H)"],
        "forms": [
            {
                "name": "base",
                "types": ["Fire", "Flying"],
                "stats": {"hp": 78, "atk": 84, "def": 78, "spa": 109, "spd": 85, "spe": 100},
                "abilities": ["Blaze", "Solar Power (H)"],
                "moves": [{"name": "Flamethrower", "method": "lv46"}],
            },
            {
                "name": "mega-x",
                "types": ["Fire", "Dragon"],
                "stats": {"hp": 78, "atk": 130, "def": 111, "spa": 130, "spd": 85, "spe": 100},
                "abilities": ["Tough Claws"],
                "moves": [],
            },
        ],
    }
    result = format_pokemon_md(data)
    assert "[mega-x] Type: Fire / Dragon" in result
    assert "HP 78 | ATK 130 | DEF 111 | SPA 130 | SPD 85 | SPE 100" in result
    assert "Abilities: Tough Claws" in result


from update_pokedex import format_index_entry


def test_format_index_entry():
    data = {
        "id": 6,
        "names": {"en": "Charizard", "ja-Hrkt": "リザードン", "zh-Hant": "噴火龍"},
        "generation": 1,
        "types": ["Fire", "Flying"],
        "stats": {"hp": 78, "atk": 84, "def": 78, "spa": 109, "spd": 85, "spe": 100},
        "abilities": ["Blaze", "Solar Power (H)"],
        "forms": [
            {"name": "base", "types": ["Fire", "Flying"], "stats": {}, "abilities": [], "moves": []},
            {"name": "mega-x", "types": ["Fire", "Dragon"], "stats": {}, "abilities": [], "moves": []},
            {"name": "mega-y", "types": ["Fire", "Flying"], "stats": {}, "abilities": [], "moves": []},
        ],
    }
    result = format_index_entry(data)
    assert "#006" in result
    assert "Charizard" in result
    assert "噴火龍" in result
    assert "Fire / Flying" in result
    assert "Gen: 1" in result
    assert "HP 78" in result
    assert "Blaze" in result
    assert "Forms: mega-x, mega-y" in result


def test_format_index_entry_no_extra_forms():
    data = {
        "id": 25,
        "names": {"en": "Pikachu", "ja-Hrkt": "ピカチュウ", "zh-Hant": "皮卡丘"},
        "generation": 1,
        "types": ["Electric"],
        "stats": {"hp": 35, "atk": 55, "def": 40, "spa": 50, "spd": 50, "spe": 90},
        "abilities": ["Static", "Lightning Rod (H)"],
        "forms": [
            {"name": "base", "types": ["Electric"], "stats": {}, "abilities": [], "moves": []},
        ],
    }
    result = format_index_entry(data)
    assert "Forms:" not in result


import tempfile
from pathlib import Path
from update_pokedex import write_pokemon_file, write_index_file


def test_write_pokemon_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        pokemon_dir = Path(tmpdir) / "pokemon"
        pokemon_dir.mkdir()
        data = {
            "id": 25,
            "names": {"en": "Pikachu", "ja-Hrkt": "ピカチュウ", "zh-Hant": "皮卡丘"},
            "generation": 1,
            "types": ["Electric"],
            "stats": {"hp": 35, "atk": 55, "def": 40, "spa": 50, "spd": 50, "spe": 90},
            "abilities": ["Static", "Lightning Rod (H)"],
            "forms": [
                {
                    "name": "base",
                    "types": ["Electric"],
                    "stats": {"hp": 35, "atk": 55, "def": 40, "spa": 50, "spd": 50, "spe": 90},
                    "abilities": ["Static", "Lightning Rod (H)"],
                    "moves": [{"name": "Thunderbolt", "method": "TM"}],
                }
            ],
        }
        write_pokemon_file(data, pokemon_dir)
        filepath = pokemon_dir / "025.md"
        assert filepath.exists()
        content = filepath.read_text(encoding="utf-8")
        assert "#025 Pikachu" in content


def test_write_index_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        data_dir = Path(tmpdir)
        all_pokemon = [
            {
                "id": 1,
                "names": {"en": "Bulbasaur", "zh-Hant": "妙蛙種子"},
                "generation": 1,
                "types": ["Grass", "Poison"],
                "stats": {"hp": 45, "atk": 49, "def": 49, "spa": 65, "spd": 65, "spe": 45},
                "abilities": ["Overgrow", "Chlorophyll (H)"],
                "forms": [{"name": "base", "types": [], "stats": {}, "abilities": [], "moves": []}],
            },
            {
                "id": 4,
                "names": {"en": "Charmander", "zh-Hant": "小火龍"},
                "generation": 1,
                "types": ["Fire"],
                "stats": {"hp": 39, "atk": 52, "def": 43, "spa": 60, "spd": 50, "spe": 65},
                "abilities": ["Blaze", "Solar Power (H)"],
                "forms": [{"name": "base", "types": [], "stats": {}, "abilities": [], "moves": []}],
            },
        ]
        write_index_file(all_pokemon, data_dir)
        filepath = data_dir / "index.md"
        assert filepath.exists()
        content = filepath.read_text(encoding="utf-8")
        assert "# Pokedex Index" in content
        assert "#001 Bulbasaur" in content
        assert "#004 Charmander" in content
