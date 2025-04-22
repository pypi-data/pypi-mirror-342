from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from pokime_helpers import get_pokemon_info, compare_pokemon, get_rich_anime_info, format_pokemon_info

load_dotenv()

mcp = FastMCP("pokime")

@mcp.tool()
async def pokemon_info(name: str) -> str:
    """Get detailed Pokémon info."""
    info = get_pokemon_info(name)
    return format_pokemon_info(info) if info else f"Could not find Pokémon '{name}'."

@mcp.tool()
async def compare_pokemon_info(pokemon1: str, pokemon2: str) -> str:
    """Compare two Pokémon by name."""
    return compare_pokemon(pokemon1, pokemon2)

@mcp.tool()
async def rich_anime_info(title: str) -> str:
    """Get richer, multi-format anime info for a title."""
    return get_rich_anime_info(title)

if __name__ == "__main__":
    mcp.run()
