#!/usr/bin/env python3
"""Write www/nowplaying.json with the YouTube track open in Firefox, for the stream overlay."""
import glob, json, os, re, time
import lz4.block

WWW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "www")
STORES = os.path.expanduser("~/Library/Application Support/Firefox/Profiles/*/sessionstore-backups/recovery.jsonlz4")
NOISE = re.compile(r"\s*[\(\[](official\s*)?(m/?v|music video|lyrics?|audio|official.*?)[\)\]]", re.I)


def read_store(path):
    with open(path, "rb") as f:
        raw = f.read()
    return json.loads(lz4.block.decompress(raw[8:]))


def current_track():
    best = None
    for path in glob.glob(STORES):
        for win in read_store(path).get("windows", []):
            for tab in win.get("tabs", []):
                entry = tab["entries"][tab.get("index", 1) - 1] if tab.get("entries") else {}
                if "youtube.com/watch" not in entry.get("url", ""):
                    continue
                if best is None or tab.get("lastAccessed", 0) > best[0]:
                    best = (tab.get("lastAccessed", 0), entry.get("title", ""))
    if not best:
        return ""
    title = re.sub(r"\s*-\s*YouTube$", "", best[1])
    return NOISE.sub("", title).strip()


while True:
    try:
        track = current_track()
    except Exception:
        track = ""
    tmp = os.path.join(WWW, ".nowplaying.json")
    with open(tmp, "w") as f:
        json.dump({"track": track}, f, ensure_ascii=False)
    os.replace(tmp, os.path.join(WWW, "nowplaying.json"))
    time.sleep(5)
