#!/usr/bin/env python3
"""Builds logos.json, the index StreamPulse reads to give channels their logo.

Sources, in this order of preference:
  1. logos/<country>/<name>-<suffix>.png in this repository (yours: they win over the same file below).
  2. tv-logo/tv-logos, pinned to the commit in sources.json so its URLs never change under the app.

Each logo gets the names it answers to: the file name in words ("espn-2-ar.png" -> "espn 2"), the usual
Movistar Plus+ forms for "<x>-por-movistar-plus" files, and the extra names in aliases.json. The app cleans
both sides the same way (case, accents, HD/SD/4K/RAW/VIP tags, "ES:" prefixes) and only takes an EXACT match,
so "ESPN" never picks "ESPN 2". A family's plain logo wins over its -hd, -hz, -uhd and -4k variants.

Usage: python3 tools/build_index.py   (GITHUB_TOKEN in the environment avoids the API rate limit)
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OWN_BASE = "https://raw.githubusercontent.com/luisgustavoluis/streampulse-logos/main/logos/"
VARIANT = re.compile(r"-(hd|hz|uhd|4k)(?=-[a-z]+\.png$)")


def tv_logos_files(repo, sha, countries):
    url = f"https://api.github.com/repos/{repo}/git/trees/{sha}?recursive=1"
    request = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "streampulse-logos"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=60) as response:
        tree = json.load(response)
    if tree.get("truncated"):
        sys.exit("tv-logos tree came back truncated")
    files = {}
    for item in tree["tree"]:
        path = item["path"]
        parts = path.split("/")
        if item["type"] == "blob" and len(parts) == 3 and parts[0] == "countries" and parts[1] in countries \
                and path.endswith(".png"):
            rel = f"{parts[1]}/{parts[2]}"
            files[rel] = 0
    return files


def own_files(countries):
    files = {}
    for country in countries:
        folder = ROOT / "logos" / country
        for png in sorted(folder.glob("*.png")) if folder.is_dir() else []:
            rel = f"{country}/{png.name}"
            files[rel] = 1
    return files


def names_for(rel, suffix):
    stem = rel.split("/", 1)[1][:-4].lower()
    if stem.endswith("-" + suffix):
        stem = stem[: -len(suffix) - 1]
    words = re.sub(r"[-_ ]+", " ", stem).strip()
    words = re.sub(r"\s*\bhz\b", "", words).strip()       # "-hz-": the horizontal version of the same logo
    names = {words}
    movistar = re.fullmatch(r"(.+) por movistar plus", words)
    if movistar:
        x = movistar.group(1)
        xs = {x}
        if x.startswith("laliga tv") and "hypermotion" not in x:   # "LaLiga TV 2 por M+" is listed as "Movistar LaLiga 2"
            xs.add(re.sub(r"^laliga tv", "laliga", x))
        forms = {f"{p} {v}" for v in xs for p in ("movistar", "movistar plus", "m plus", "m")}
        if not re.search(r"\d$", x):          # the first of a numbered family is often listed as "... 1"
            forms |= {f + " 1" for f in forms}
        names |= forms
    return names


def main():
    sources = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
    aliases = json.loads((ROOT / "aliases.json").read_text(encoding="utf-8"))
    countries = sources["countries"]
    files = tv_logos_files(sources["tvLogos"]["repo"], sources["tvLogos"]["sha"], countries)
    own = own_files(countries)
    files.update(own)                         # yours replace the same file from tv-logos
    unknown = sorted(set(aliases) - set(files))
    if unknown:
        sys.exit(f"aliases.json names logos that do not exist: {unknown}")
    logos = []
    for rel in sorted(files):
        base = VARIANT.sub("", rel)
        if base != rel and base in files and rel not in own and rel not in aliases:
            continue
        country = rel.split("/", 1)[0]
        names = names_for(rel, countries[country]["suffix"]) | {a.strip() for a in aliases.get(rel, []) if a.strip()}
        logos.append({"b": files[rel], "p": urllib.parse.quote(rel), "c": countries[country]["code"], "n": sorted(names)})
    repo, sha = sources["tvLogos"]["repo"], sources["tvLogos"]["sha"]
    # A logo's URL is bases[b] + p: tv-logos pinned to a commit (0) or this repository (1).
    bases = [f"https://raw.githubusercontent.com/{repo}/{sha}/countries/", OWN_BASE]
    index = {"version": 1, "bases": bases, "logos": logos}
    out = ROOT / "logos.json"
    out.write_text(json.dumps(index, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"logos.json: {len(logos)} logos ({len(own)} own), {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()
