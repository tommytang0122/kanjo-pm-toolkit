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
