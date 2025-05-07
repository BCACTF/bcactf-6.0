#!/usr/bin/env python3
"""
Public 5MF Generator for the 5D Printer Challenge

This script reads the flag from standard input and generates a scrambled 5MF file.
The commands are intentionally output in a random order so that the correct ordering
must be recovered by sorting by the extra dimensions.

The printer is “5D” because, in addition to X, Y, and Z (with Z always 0 here),
each command carries:
    U = (subpath_index * 100) + (t * 100)
    V = 50 * sin(2*pi*t)
where t is the normalized progression along that command segment.
    
Usage:
    python publish_me_generate_5mf.py
Then paste the flag string when prompted.
"""

import sys, math, random
import numpy as np
from matplotlib.textpath import TextPath
from matplotlib.path import Path

def main():
    flag = input("Enter the flag text: ").strip()
    # Generate a vector outline from the provided flag text.
    tp = TextPath((0, 0), flag, size=100)
    vs = tp.vertices
    cs = tp.codes

    # Group the vertices into subpaths (each starting with MOVETO)
    subs = []
    cur = []
    for coord, code in zip(vs, cs):
        if code == Path.MOVETO:
            if cur:
                subs.append(cur)
            cur = [(coord[0], coord[1], code)]
        else:
            cur.append((coord[0], coord[1], code))
    if cur:
        subs.append(cur)

    cmds = []  # list to store each command (dict with keys: code, X, Y, Z, U, V)
    for sid, sub in enumerate(subs):
        tot = 0.0
        last_x, last_y, _ = sub[0]
        segs = [0.0]  # first command, distance is zero
        for (x, y, _) in sub[1:]:
            d = math.hypot(x - last_x, y - last_y)
            tot += d
            segs.append(d)
            last_x, last_y = x, y
        cum = 0.0
        for i, (x, y, code) in enumerate(sub):
            if i > 0:
                cum += segs[i]
            # t goes from 0 to 1 along the subpath. (When tot==0, t remains 0.)
            t = cum/tot if tot > 0 else 0.0
            # Unique twist: use subpath index so that commands from later subpaths always have higher U.
            u = (sid * 100) + (t * 100)
            # V is a cyclic parameter (could represent, say, a material property over time).
            v = 50.0 * math.sin(2 * math.pi * t)
            # Z is maintained 0 for a 2D layer.
            cmds.append({
                "code": code,
                "X": x,
                "Y": y,
                "Z": 0.0,
                "U": u,
                "V": v
            })

    # Scramble the ordering so that the proper toolpath order is hidden.
    random.shuffle(cmds)

    # Write out in a custom 5MF format.
    outfile = "flag.5mf"
    with open(outfile, "w") as f:
        f.write("; 5D Printer file (5MF format)\n")
        f.write("G5D_INIT\n")
        for c in cmds:
            # Use G5D_MOVE for MOVETO commands, G5D_DRAW otherwise.
            op = "G5D_MOVE" if c["code"] == Path.MOVETO else "G5D_DRAW"
            f.write("{} X{:.3f} Y{:.3f} Z{:.3f} U{:.3f} V{:.3f}\n".format(op, c["X"], c["Y"], c["Z"], c["U"], c["V"]))
        f.write("G5D_END\n")
    print(f"[+] 5MF file generated: {outfile}")

if __name__ == "__main__":
    main()
