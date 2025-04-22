import requests

def get_pokemon_info(name: str) -> dict | None:
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()
    return {
        "name": data["name"].title(),
        "types": [t["type"]["name"] for t in data["types"]],
        "abilities": [a["ability"]["name"] for a in data["abilities"]],
        "height": data["height"],
        "weight": data["weight"],
        "base_stats": {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]}
    }

def format_pokemon_info(info: dict) -> str:
    stats = "\n".join([f"  {k.title()}: {v}" for k, v in info["base_stats"].items()])
    return (
        f"Name: {info['name']}\n"
        f"Types: {', '.join(info['types'])}\n"
        f"Abilities: {', '.join(info['abilities'])}\n"
        f"Height: {info['height']} | Weight: {info['weight']}\n"
        f"Base Stats:\n{stats}"
    )

def compare_pokemon(pokemon1: str, pokemon2: str) -> str:
    p1 = get_pokemon_info(pokemon1)
    p2 = get_pokemon_info(pokemon2)

    if not p1 or not p2:
        return "One or both Pokémon not found."

    p1_str = format_pokemon_info(p1)
    p2_str = format_pokemon_info(p2)

    return f"--- {p1['name']} ---\n{p1_str}\n\n--- {p2['name']} ---\n{p2_str}"

def get_rich_anime_info(title: str) -> str:
    query = '''
    query ($search: String) {
      Page(page: 1, perPage: 5) {
        media(search: $search, type: ANIME) {
          title {
            romaji
            english
          }
          format
          episodes
          status
          genres
          averageScore
          startDate {
            year
          }
          description(asHtml: false)
        }
      }
    }
    '''
    variables = {"search": title}
    url = "https://graphql.anilist.co"
    response = requests.post(url, json={"query": query, "variables": variables})

    if response.status_code != 200:
        return f"Could not find info for anime '{title}'."

    media_list = response.json()["data"]["Page"]["media"]
    if not media_list:
        return "No anime found."

    formatted = []
    for m in media_list:
        description = (m["description"] or "No description")[:300].replace("\n", " ") + "..."
        formatted.append(
            f"Title: {m['title']['english'] or m['title']['romaji']}\n"
            f"Format: {m['format']} | Episodes: {m['episodes'] or 'N/A'} | Status: {m['status']}\n"
            f"Genres: {', '.join(m['genres'])}\n"
            f"Average Score: {m['averageScore']} | Year: {m['startDate']['year']}\n"
            f"Description: {description}"
        )

    return "\n\n---\n\n".join(formatted)
