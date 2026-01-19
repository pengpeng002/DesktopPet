# Project: Live2D Desktop Pet Application

## Project Overview

This project is a Live2D desktop pet application that brings an interactive Live2D character to the user's desktop. It leverages a hybrid approach, combining a Python-based desktop wrapper with a web-based frontend for rendering and interaction. The application features a frameless, transparent, and always-on-top window displaying a Live2D model that can animate, speak with lip-sync, and track the user's mouse movements. A utility script is included to manage the character's voice lines and subtitles.

**Key Technologies:**

*   **Python (PyQt5/PyQt6)**: For creating the desktop window, managing window properties (frameless, transparent, always-on-top), and embedding the web content.
*   **HTML/CSS/JavaScript**: For the interactive Live2D display, including:
    *   **PixiJS**: A 2D rendering engine.
    *   **Live2D Cubism SDK**: For loading, rendering, and animating Live2D models.
    *   **WebEngine (Chromium)**: Embedded within the PyQt application to render the web content.

## Architecture

The application consists of two main parts:

1.  **Python Desktop Wrapper (`main.py`)**:
    *   Initializes a PyQt application and `QMainWindow`.
    *   Sets window flags for a frameless, transparent, and always-on-top window.
    *   Uses `QWebEngineView` to load `index2.html`.
    *   Handles drag-to-move functionality for the window.
    *   Monitors keyboard input (e.g., `ESC` to quit).
    *   Periodically sends mouse cursor coordinates to the embedded web view's JavaScript to enable eye-tracking.
    *   Allows JavaScript to signal the Python application for actions like quitting.

2.  **Web Frontend (`index2.html`)**:
    *   Uses PixiJS and Live2D libraries to display and animate a Live2D model.
    *   Loads the model (`lafei_4` by default) and its associated motion and texture data.
    *   Implements interactive elements, such as playing specific motions on click.
    *   Features lip-syncing for character speech and displays corresponding subtitles.
    *   Includes a custom right-click context menu for selecting motions and an option to exit the application (which communicates back to the Python wrapper).
    *   Contains hardcoded `voiceMap` and `voiceTextMap` to link motions, audio files, and subtitle text.

## Utilities

*   **`get_sound.py`**: A Python script designed to scrape character voice line URLs and their corresponding text from a given HTML string. It downloads these MP3 files and generates a `voice_map.json` file, which maps audio filenames to subtitle text. This script is used for preparing the data consumed by the web frontend.

## Building and Running

**Prerequisites:**

*   Python (3.x recommended)
*   `pip` (Python package installer)

**Setup:**

1.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
    (On Linux/macOS, use `source venv/bin/activate`)

2.  **Install Dependencies:**
    The project uses PyQt for the desktop application and `requests`, `BeautifulSoup4` for the `get_sound.py` script.
    ```bash
    pip install PyQt5 # Or PyQt6, depending on your environment. main.py currently imports PyQt5 but venv shows PyQt6.
    pip install requests beautifulsoup4
    ```

**Preparing Sound Data (Optional, if `sound` folder and `voice_map.json` are missing/outdated):**

```bash
python get_sound.py
```
This will download MP3 files into a `sound/` directory and create a `voice_map.json`.

**Running the Application:**

```bash
python main.py
```

## Development Conventions

*   **Python:** Uses PyQt for desktop integration.
*   **Web Frontend:** Standard HTML, CSS, JavaScript using PixiJS and Live2D libraries. Dependencies are loaded via CDN in `index2.html`.
*   **Voice/Subtitle Data:** Managed by `get_sound.py`, which populates `sound/` and `voice_map.json`. The `voiceMap` and `voiceTextMap` in `index2.html` are manually updated based on the output of `get_sound.py` or directly hardcoded.
*   **Model Data:** Live2D model files (e.g., `.moc3`, `.model3.json`, `.physics3.json`, textures) are expected to be in a dedicated folder (e.g., `lafei_4/`).

## Known Issues / TODOs

*   **PyQt Version Inconsistency:** `main.py` imports `PyQt5`, but the provided `venv` directory indicates `PyQt6` is installed. This might lead to compatibility issues if not addressed. Ensure the correct PyQt version is installed and imported.
*   **Hardcoded Data in HTML**: `index2.html` contains hardcoded `voiceMap` and `voiceTextMap`. While `get_sound.py` generates `voice_map.json`, there's no direct mechanism shown for `index2.html` to dynamically load `voice_map.json` or to generate the `voiceTextMap` from it. This suggests manual synchronization is currently required. Consider implementing dynamic loading of `voice_map.json` in `index2.html`.
*   **Model Switching**: The `MODEL_NAME` in `index2.html` is hardcoded. To switch models, this line needs manual editing. A more dynamic approach could be implemented.
