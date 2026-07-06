# 🏗️ Prism Player Architecture

This document serves as a high-level overview of the Prism Player codebase. It's meant to help new contributors quickly understand where things are located and how the components interact.

## Directory Structure

```text
musicbeast/
├── main.py                # Entry point & Main Application Loop
├── README.md              # Project overview
├── build.sh               # PyInstaller build script
├── requirements.txt       # Python dependencies
├── .github/               # GitHub issue/PR templates
├── docs/                  # Documentation
└── prism/                 # Core Package
    ├── api/               # External APIs & Data Fetching
    │   ├── aggregator.py  # Unified API for YouTube, SoundCloud, Local & LRCLIB
    │   └── mpris.py       # DBus integration for Linux Media Controls
    ├── core/              # State, Config, and Logic
    │   ├── config.py      # Saving/Loading settings.json & Paths
    │   ├── history.py     # LRU Cache for playback history
    │   ├── playlists.py   # JSON-based custom playlists logic
    │   ├── system.py      # PulseAudio/ALSA volume & libnotify
    │   └── themes.py      # Color schemes using rich.theme.Theme
    ├── graphics.py        # Terminal Visuals
    │   # ASCII generation from Images, CAVA data smoothing, etc.
    └── ui/                # Terminal Rendering
        ├── components.py  # Reusable UI parts (Header, Mini-player)
        └── views.py       # Full-screen layouts (Player, Dashboard, Settings)
```

## How It Works

1. **The Event Loop (`main.py`)**: 
   The application is driven by a single `while True:` loop wrapped in a `blessed.Terminal()` context. It handles keyboard events using `term.inkey()`.
   
2. **UI Rendering (`prism/ui/`)**: 
   Every frame, the active layout is generated using the `rich` library (e.g., `Layout`, `Panel`, `Text`). The resulting layout is passed to a `rich.live.Live` instance for flicker-free terminal rendering.

3. **Audio Playback**: 
   Audio is handled entirely via `ffplay` running as a daemon subprocess (`subprocess.Popen`). This prevents the Python GIL from blocking the audio stream.

4. **Background Tasks (`prism/api/`)**: 
   Heavy operations like fetching covers (`download_cover_to_cache`), scraping lyrics, or parsing YouTube metadata are dispatched to background daemon threads (`threading.Thread`). This ensures the UI never freezes while waiting for network IO.

5. **MPRIS Control (`prism/api/mpris.py`)**: 
   A dedicated thread runs a `GLib.MainLoop` attached to the Linux Session Bus. It exposes a standard `org.mpris.MediaPlayer2` interface, allowing desktop environments and media keys to control Prism Player seamlessly.

## Adding a New Theme
Themes are simple dictionaries defined in `prism/core/themes.py`. To add a new one, define `primary`, `secondary`, and `tertiary` hex colors, and PR it!

## Extending the Aggregator
`prism/api/aggregator.py` exposes standard `search_all` and `get_stream_info` functions. To add a new music source (e.g., Spotify), implement a search function that returns a unified dictionary format, and add it to `search_all`.
