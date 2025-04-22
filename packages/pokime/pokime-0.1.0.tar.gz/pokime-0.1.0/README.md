# Pokime 🎮📺

**Pokime** is an MCP (Model Context Protocol) server that allows LLMs to retrieve rich information about **Pokémon** and **anime** titles in real-time. You can get detailed Pokémon stats, compare two Pokémon, and explore multi-season anime metadata from AniList.

---

## ✨ Features

- 🔍 **Pokémon Lookup** – Type, abilities, base stats, height, and weight.
- ⚔️ **Pokémon Comparison** – Side-by-side detail of two Pokémon.
- 📺 **Anime Info (via AniList)** – Format, episodes, genres, ratings, descriptions across all seasons and formats.

---

## 🧱 Tech Stack

- [PokéAPI](https://pokeapi.co/) for Pokémon data
- [AniList GraphQL API](https://anilist.gitbook.io/) for anime data
- Python 3.10+
- `.env` config support with `python-dotenv`

---
## How to add 
```
"pokime": {
    "command": "uv",
    "args": [
        "run",
        "pokime.py"
      ]
    }
```
