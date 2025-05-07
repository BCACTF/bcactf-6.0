#!/usr/bin/env python3
"""
Verification Tool for the 5D Printer Challenge

This script reads a 5MF file (produced by the public generator) and:
  1. Sorts the G5D commands by U and then by V to recover the proper toolpath order.
  2. Renders two plots:
       - The X–Y toolpath (which should display the flag).
       - A timeline visualization (plotting U vs. V).
       
Usage:
    python verify_and_render_5mf.py
"""

import sys, math
import matplotlib.pyplot as plt

def load_5mf(filename="flag.5mf"):
    commands = []
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith(";") or not line:
                    continue
                parts = line.split()
                cmd = parts[0]
                params = {}
                for part in parts[1:]:
                    key = part[0]
                    try:
                        params[key] = float(part[1:])
                    except ValueError:
                        params[key] = part[1:]
                commands.append((cmd, params))
    except FileNotFoundError:
        print("[!] File not found:", filename)
        sys.exit(1)
    return commands

def render_5mf(filename="flag.5mf"):
    # Load commands from file
    cmds = load_5mf(filename)
    # Sort commands based on U (primary) then V (secondary)
    sorted_cmds = sorted(cmds, key=lambda x: (x[1].get("U", 0), x[1].get("V", 0)))

    # Reconstruct the drawing path by following the sorted commands.
    drawing_segments = []
    timeline_pts = []
    curr_x, curr_y = None, None
    for cmd, params in sorted_cmds:
        # Collect timeline data
        if "U" in params and "V" in params:
            timeline_pts.append((params["U"], params["V"]))
        if cmd == "G5D_MOVE":
            curr_x = params.get("X", None)
            curr_y = params.get("Y", None)
        elif cmd == "G5D_DRAW":
            x_new = params.get("X", None)
            y_new = params.get("Y", None)
            if curr_x is not None and curr_y is not None:
                drawing_segments.append(([curr_x, x_new], [curr_y, y_new]))
            curr_x, curr_y = x_new, y_new
        # Other commands like G5D_INIT and G5D_END are ignored.

    # Create two subplots: one for the drawing (X–Y) and one for the timeline (U–V).
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Plot the reconstructed toolpath.
    for seg in drawing_segments:
        ax1.plot(seg[0], seg[1], color="red", lw=1)
    ax1.set_title("Reconstructed 5D Printer Toolpath (X–Y)")
    ax1.set_xlabel("X")
    ax1.set_ylabel("Y")
    ax1.axis("equal")
    ax1.grid(True)

    # Plot the timeline (U vs. V).
    if timeline_pts:
        U_vals, V_vals = zip(*timeline_pts)
        ax2.plot(U_vals, V_vals, marker="o", linestyle="-", color="blue")
        ax2.set_title("Timeline (U vs. V)")
        ax2.set_xlabel("U (Primary: timestamp/subpath offset)")
        ax2.set_ylabel("V (Cyclic property)")
        ax2.grid(True)
    else:
        ax2.text(0.5, 0.5, "No timeline data available", ha="center", va="center")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    render_5mf()
