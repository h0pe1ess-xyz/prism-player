<div align="center">

```text
    ____       _                 ____  __                       
   / __ \_____(_)TT____ _____   / __ \/ /___ ___  _____  _____
  / /_/ / ___/ / ___/ __ `__ \ / /_/ / / __ `/ / / / _ \/ ___/
 / ____/ /  / (__  ) / / / / // ____/ / /_/ / /_/ /  __/ /    
/_/   /_/  /_/____/_/ /_/ /_//_/   /_/\__,_/\__, /\___/_/     
                                           /____/             
```

**A fully featured, terminal-based music player and aggregator for Linux.**

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)](https://www.python.org/)
[![Made with Love](https://img.shields.io/badge/Made%20with-❤️-red.svg)](#)

</div>

<br />

Listen to music from **YouTube**, **SoundCloud**, and your **local library** directly from your terminal with a stunning, customizable UI. Prism Player is designed to be lightweight, incredibly fast, and visually beautiful using pure terminal ASCII art and animations.

---

## ✨ Features

* 🌍 **Multi-Source Aggregation:** Search and stream tracks from YouTube and SoundCloud without leaving your terminal.
* 📂 **Local Music:** Automatically scan and play `.mp3`, `.flac`, `.wav`, and `.m4a` files from your `~/Music` directory.
* 🎤 **Synchronized Lyrics:** Automatically fetches and displays real-time synchronized lyrics via LRCLIB.
* 🎛️ **Audio FX & Equalizer:** Apply real-time effects like Nightcore and Slowed+Reverb, or adjust the built-in Bass & Treble EQ.
* 📊 **Cava Visualizer:** Stunning audio visualizations integrated directly into the UI.
* 🖥️ **MPRIS Integration:** Seamlessly integrates with Linux Desktop Environments (KDE, GNOME, etc.). Use your media keys or `playerctl`.
* 🎮 **Discord Rich Presence:** Show off what you're listening to on Discord automatically.
* 🎨 **Premium Themes:** Includes Cyberpunk, Matrix, Sunset, Dracula, Nord, Gruvbox, and Catppuccin themes.
* 📱 **Mini-Mode:** Press `M` to collapse the player into a compact, space-saving layout!

## 📦 Installation

Prism Player relies on `ffplay` (from `ffmpeg`) for robust audio streaming and `playerctl` for system MPRIS integration.

### 1. Install System Dependencies (Linux)
```bash
# Debian/Ubuntu
sudo apt update
sudo apt install ffmpeg playerctl
```

### 2. Clone & Setup
```bash
git clone https://github.com/h0pe1ess/musicbeast.git
cd musicbeast
pip install -r requirements.txt
```

### 3. Run the Player
```bash
python main.py
```

---

## 🛠️ Build Standalone Binary

You can compile Prism Player into a single, portable binary. No Python environment needed!

```bash
bash build.sh
./dist/prism_player
```

---

## ⌨️ Controls & Keybinds

Prism Player is fully keyboard-driven. 

| Key | Action | Context |
| :---: | :--- | :--- |
| `Space` | Pause / Resume | Global |
| `TAB` | Switch between Dashboard / Player | Global |
| `M` | Toggle Mini Mode | Global |
| `/` | Open Search | Global |
| `P` | Open Playlists | Global |
| `S` | Open Settings | Global |
| `N` | Next Track | Global |
| `B` | Previous Track | Global |
| `-` / `+` | Volume Down / Up | Global |
| `Left/Right` | Seek +/- 5 seconds | Player View |
| `L` | Toggle Lyrics | Player View |
| `E` | Open Equalizer | Player View |
| `R` | Toggle Repeat | Player View |
| `A` | Add to Playlist | Player View |
| `Q` | Quit Application | Global |

---

## 🏗️ Architecture

Prism Player is built with a modular, scalable architecture:
* `main.py`: Entry point and main event loop.
* `prism/api/`: Data aggregation (YouTube, SoundCloud, Local).
* `prism/ui/`: UI components, views, and rendering logic (`rich` + `blessed`).
* `prism/core/`: System integration, configuration, and player state.
* `prism/graphics.py`: ASCII art generation and Cava integration.

## 📄 License

This project is licensed under the **GPLv3 License** - see the [LICENSE](LICENSE) file for details.

---
<div align="center">
  <i>Created by <b>h0pe1ess</b></i>
</div>
