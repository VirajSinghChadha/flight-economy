# ✈️ Flight Economy Simulator

A single-file browser game where you build an airline (and a shipping/cruise line) from $1M into a global giant.
Inspired by the Roblox game *Run an Airline* and by *Fly Corp*. **Not affiliated with either.**

**▶ Play:** https://virajsinghchadha.github.io/flight-economy/  (or just open `index.html` in any browser)

## Features
- **4,226 real cities with airports** on a world map; demand depends on population, destination appeal (Paris, Dubai, Las Vegas…), region and distance
- **Passenger & cargo aircraft** (Cessna Caravan → A380, 747-8F…) with different icons, colours and sizes
- **Ships:** ferries and cruise ships between ports ⚓
- **Weather**, wars, volcanoes, storms and protests that close airspace and airports (refunds, airport fees, damage)
- Maintenance (compulsory below 15%, optional auto-service), staff pay & strikes, loans, airport capacity & hubs, **transfer passengers**
- **IPO**: pick how much of the company to keep; a **board of directors** makes demands, blocks decisions when unhappy, and can fire you if you own less than half
- **Rival airlines** with real networks: they can recruit saboteurs (leaks, smear campaigns, cyber-attacks, aircraft sabotage); you can defend, press charges, buy them out — or try covert operations yourself (get caught and face sanctions)
- Scenarios, daily challenges, random good/bad/funny events, reputation campaigns, route suggestions, search
- First-time **tutorial**

## Saves & updates
- Progress is saved automatically in your browser (localStorage) and **carries over updates** — new fields are filled in with defaults when an old save loads.
- Use **Airline → Export save / Import save** to back up or move your save (the website and a local file have separate browser storage).
- The game checks `version.json` on this repo and shows an **update banner** when a newer version is published.

## Build
```
python3 src/build.py      # builds index.html from src/game.src.html + src/data.json
```
`src/build_data.py` regenerates `data.json` from GeoNames, OpenFlights and Natural Earth files.

To release an update: edit `src/game.src.html`, bump `VERSION` there **and** in `version.json`, rebuild, commit and push.

## Data credits
- Cities (population ≥ 100k): [GeoNames](https://www.geonames.org/) — CC BY 4.0
- Airports & routes: [OpenFlights](https://openflights.org/data.html) — Open Database License (ODbL)
- Coastlines: [Natural Earth](https://www.naturalearthdata.com/) (via `world-atlas`) — public domain

All crises, rivals, scandals and covert operations are **fictional game mechanics**, not statements about real places or companies.

Code: MIT.
