import json
import os
import time

HISTORY_DIR = os.path.expanduser("~/.musicbeast")
HISTORY_FILE = os.path.join(HISTORY_DIR, "history.json")
MAX_HISTORY = 50


def _ensure_dir():
    os.makedirs(HISTORY_DIR, exist_ok=True)


def get_history(limit=20):
    """Returns last N tracks from listening history, newest first."""
    _ensure_dir()
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data[:limit]
    except (json.JSONDecodeError, IOError):
        return []


def add_to_history(track_id, title, artist, source="youtube", thumbnails=None):
    """Adds a track to listening history. Moves to top if already exists."""
    if not track_id:
        return
    _ensure_dir()
    history = get_history(MAX_HISTORY)

    # Remove duplicates (move to front instead)
    history = [h for h in history if h.get("id", h.get("videoId")) != track_id]

    # Insert at front
    entry = {
        "id": track_id,
        "title": title,
        "artist": artist,
        "source": source,
        "thumbnails": thumbnails or [],
        "timestamp": time.time()
    }
    history.insert(0, entry)

    # Trim to max
    history = history[:MAX_HISTORY]

    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except IOError:
        pass
