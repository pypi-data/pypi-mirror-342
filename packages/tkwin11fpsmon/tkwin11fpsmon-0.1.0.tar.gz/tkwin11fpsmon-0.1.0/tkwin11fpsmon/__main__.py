# File: fpsmon.py

import argparse
import sys
import time
import ctypes

import win32api
import win32con
import tkinter as tk

# ─── Initialize DWM API ───────────────────────────────
# API for synchronizing with Desktop Window Manager frame completion
_dwm = ctypes.WinDLL("dwmapi")
DwmFlush = _dwm.DwmFlush


def list_monitors():
    """
    Enumerate connected monitors in the order returned by EnumDisplayMonitors,
    and return a list of tuples:
    [(num, DeviceName, DeviceString, (left, top, right, bottom)), ...].
    `num` is a 1-based index.
    """
    # 1) Get monitor handles and rectangles
    entries = []
    for hMon, _, _ in win32api.EnumDisplayMonitors(None, None):
        info = win32api.GetMonitorInfo(hMon)
        entries.append((info["Device"], info["Monitor"]))

    # 2) Build a map from DeviceName to description string via EnumDisplayDevices
    desc_map = {}
    idx = 0
    while True:
        try:
            dev = win32api.EnumDisplayDevices(None, idx)
        except Exception:
            break
        if dev.StateFlags & win32con.DISPLAY_DEVICE_ATTACHED_TO_DESKTOP:
            desc_map[dev.DeviceName] = dev.DeviceString
        idx += 1

    # 3) Assign 1-based indices and return the list
    monitors = []
    for i, (name, rect) in enumerate(entries):
        desc = desc_map.get(name, "")
        monitors.append((i + 1, name, desc, rect))
    return monitors


def show_identifiers(monitors, duration_ms=3000):
    """
    - Print the monitor list to the console
    - Display an overlay with numbers 1..N at the center of each monitor for duration_ms milliseconds
    """
    print("=== Available Displays (Monitor Order) ===")
    for num, name, desc, _ in monitors:
        print(f"{num}. {name} → {desc}")
    print("\nUsage examples:")
    print("  py fpsmon.py -display 1")
    print("  py fpsmon.py -display \"\\\\.\\DISPLAY2\" -t 60")
    print("  py fpsmon.py -display 1 -unlimited\n")

    root = tk.Tk()
    root.withdraw()

    windows = []
    for num, _, _, rect in monitors:
        left, top, right, bottom = rect
        width, height = right - left, bottom - top

        win = tk.Toplevel(root)
        win.overrideredirect(True)
        win.attributes('-topmost', True)
        win.configure(bg='black')
        x = left + (width // 2) - 150
        y = top + (height // 2) - 100
        win.geometry(f"300x200+{x}+{y}")

        lbl = tk.Label(
            win,
            text=str(num),
            font=("Helvetica", 48, "bold"),
            fg="white",
            bg="black"
        )
        lbl.pack(expand=True, fill="both")
        windows.append(win)

    def close_all():
        for w in windows:
            w.destroy()
        root.quit()

    root.after(duration_ms, close_all)
    root.mainloop()


def show_fps_overlay(monitors, selection, duration_s, unlimited):
    """
    Overlay the measured FPS / configured refresh rate on a specified monitor.
    selection: 1-based index or DeviceName (string)
    duration_s: duration in seconds (None for unlimited)
    """
    # 1) Determine the target monitor
    target = None
    for num, name, desc, rect in monitors:
        if (isinstance(selection, int) and num == selection) or (selection == name):
            target = (num, name, desc, rect)
            break
    if target is None:
        print(f"Error: Monitor '{selection}' not found.")
        sys.exit(1)
    _, name, _, rect = target

    # 2) Get the configured refresh rate
    dm = win32api.EnumDisplaySettings(name, win32con.ENUM_CURRENT_SETTINGS)
    configured = dm.DisplayFrequency

    # 3) Create the overlay window
    left, top, right, bottom = rect
    width, height = right - left, bottom - top

    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    root.configure(bg='black')
    x = left + (width // 2) - 100
    y = top + (height // 2) - 50
    root.geometry(f"200x100+{x}+{y}")

    lbl = tk.Label(
        root,
        text="--/--",
        font=("Helvetica", 32, "bold"),
        fg="lime",
        bg="black"
    )
    lbl.pack(expand=True, fill="both")

    # 4) Frame synchronization count using DwmFlush
    start = time.time()
    last = start
    count = 0

    while unlimited or (time.time() - start) < duration_s:
        # Block until the next frame is completed
        DwmFlush()
        count += 1
        now = time.time()
        if now - last >= 1.0:
            fps = count
            lbl.config(text=f"{fps}/{configured}")
            count = 0
            last = now
        # Update UI
        root.update_idletasks()
        root.update()

    root.destroy()


def parse_args():
    p = argparse.ArgumentParser(description="Simple FPS monitor for Windows")
    p.add_argument(
        "-display",
        help="Specify target monitor by 1-based index or DeviceName"
    )
    p.add_argument(
        "-t", type=int, metavar="SECONDS",
        help="Number of seconds to run (default: 30)"
    )
    p.add_argument(
        "-unlimited", action="store_true",
        help="Run until manually closed (Ctrl+C to exit)"
    )
    return p.parse_args()


def main():
    args = parse_args()
    monitors = list_monitors()

    # No display specified -> show monitor index overlays
    if not args.display:
        show_identifiers(monitors)
        return

    # Interpret selection
    try:
        sel = int(args.display)
    except ValueError:
        sel = args.display

    duration = None if args.unlimited else (args.t if args.t is not None else 30)
    show_fps_overlay(monitors, sel, duration, args.unlimited)


if __name__ == "__main__":
    main()
