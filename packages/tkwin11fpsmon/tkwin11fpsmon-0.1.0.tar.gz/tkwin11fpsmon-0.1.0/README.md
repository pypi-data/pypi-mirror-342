# tkwin11fpsmon

`tkwin11fpsmon` is a minimal FPS monitor overlay for Windows 11 using `tkinter` and `DWM Flush`.  
It displays the actual screen refresh rate on a selected monitor without relying on external overlays or game hooks.

## Features

- Real-time FPS measurement based on DWM frame flush
- Simple overlay using tkinter (no external dependencies)
- Supports monitor-specific targeting
- Lightweight and privacy-friendly (no tracking)

## Installation

```
pip install tkwin11fpsmon
```

## Usage

```
tkwin11fpsmon                 # Show monitor list with overlay
tkwin11fpsmon -display 1      # Show FPS overlay on monitor 1
tkwin11fpsmon -t 60           # Run for 60 seconds
tkwin11fpsmon -unlimited      # Run until manually closed
```

## Author

Amanokawa Kaede  
GitHub: https://github.com/KAEDEAK

## License

MIT
