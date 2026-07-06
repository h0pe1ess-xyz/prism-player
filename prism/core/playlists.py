import json
import os
import uuid
import time

PLAYLISTS_DIR = os.path.expanduser("~/.musicbeast")
PLAYLISTS_FILE = os.path.join(PLAYLISTS_DIR, "playlists.json")


def _ensure_dir():
    os.makedirs(PLAYLISTS_DIR, exist_ok=True)


def _load():
    _ensure_dir()
    if not os.path.exists(PLAYLISTS_FILE):
        return []
    try:
        with open(PLAYLISTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def _save(playlists):
    _ensure_dir()
    try:
        with open(PLAYLISTS_FILE, "w", encoding="utf-8") as f:
            json.dump(playlists, f, indent=2, ensure_ascii=False)
    except IOError:
        pass


def get_all_playlists():
    """Повертає всі плейлісти."""
    return _load()


def create_playlist(name):
    """Створює новий плейліст і повертає його."""
    playlists = _load()
    new_pl = {
        "id": str(uuid.uuid4())[:8],
        "name": name,
        "created": time.time(),
        "tracks": []
    }
    playlists.append(new_pl)
    _save(playlists)
    return new_pl


def delete_playlist(playlist_id):
    """Видаляє плейліст за ID."""
    playlists = _load()
    playlists = [p for p in playlists if p["id"] != playlist_id]
    _save(playlists)


def rename_playlist(playlist_id, new_name):
    """Перейменовує плейліст."""
    playlists = _load()
    for pl in playlists:
        if pl["id"] == playlist_id:
            pl["name"] = new_name
            break
    _save(playlists)


def add_track(playlist_id, track_id, title, artist, source="youtube", thumbnails=None):
    """Додає трек у плейліст. Повертає True якщо успішно."""
    if not track_id:
        return False
    playlists = _load()
    for pl in playlists:
        if pl["id"] == playlist_id:
            # Уникаємо дублікатів
            if any(t.get("id", t.get("videoId")) == track_id for t in pl["tracks"]):
                return False
            pl["tracks"].append({
                "id": track_id,
                "title": title,
                "artist": artist,
                "source": source,
                "thumbnails": thumbnails or []
            })
            _save(playlists)
            return True
    return False


def remove_track(playlist_id, track_index):
    """Видаляє трек з плейлісту за індексом."""
    playlists = _load()
    for pl in playlists:
        if pl["id"] == playlist_id:
            if 0 <= track_index < len(pl["tracks"]):
                pl["tracks"].pop(track_index)
                _save(playlists)
                return True
    return False


def get_tracks(playlist_id):
    """Повертає треки плейлісту."""
    playlists = _load()
    for pl in playlists:
        if pl["id"] == playlist_id:
            return pl["tracks"]
    return []
