"""
Entry point for the http_apis lab practice.

Run with:
    python -m http_apis
"""

import logging
from pathlib import Path

from http_apis.pokemon_client import PokemonClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)

SPRITES_DIR = Path("sprites")

DEMO_POKEMON = ["pikachu", "bulbasaur", "charmander", "squirtle"]


def _print_section(title: str) -> None:
    print(f"\n{'=' * 55}")
    print(f"  {title}")
    print("=" * 55)


def main() -> None:
    with PokemonClient() as client:

        # ------------------------------------------------------------------
        # 1. Paginated list — shows query-param handling + retries
        # ------------------------------------------------------------------
        _print_section("1. Paginated Pokémon list (first 5)")
        listing = client.get_pokemon_list(limit=5, offset=0)
        print(f"Total Pokémon in PokéAPI: {listing['count']}")
        for entry in listing["results"]:
            print(f"  - {entry['name']}")

        # ------------------------------------------------------------------
        # 2. Individual Pokémon data — retries + timeout demo
        # ------------------------------------------------------------------
        _print_section("2. Individual Pokémon data")
        for name in DEMO_POKEMON:
            p = client.get_pokemon(name)
            types = ", ".join(t["type"]["name"] for t in p["types"])
            abilities = ", ".join(a["ability"]["name"] for a in p["abilities"])
            print(
                f"  #{p['id']:>3}  {p['name'].capitalize():<12} "
                f"types=[{types}]  abilities=[{abilities}]"
            )

        # ------------------------------------------------------------------
        # 3. Streaming sprite downloads — memory-efficient, chunk by chunk
        # ------------------------------------------------------------------
        _print_section("3. Streaming sprite downloads")
        print(f"  Destination folder: {SPRITES_DIR.resolve()}\n")

        for name in DEMO_POKEMON:
            p = client.get_pokemon(name)
            sprite_url: str | None = p["sprites"]["front_default"]

            if not sprite_url:
                print(f"  {name}: no default sprite available")
                continue

            dest = SPRITES_DIR / f"{p['id']:03d}_{p['name']}.png"
            saved = client.download_sprite(sprite_url, dest)
            size_kb = saved.stat().st_size / 1024
            print(f"  {saved.name}  ({size_kb:.1f} KB)")

    print("\nLab complete.")


if __name__ == "__main__":
    main()
