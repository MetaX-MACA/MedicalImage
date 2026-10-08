#!/usr/bin/env python3
""" Generate a directory of Plastimatch PFM DRR projections.

    All or portions of this licensed product (such portions are the "Software")
    have been obtained under license from MGH and are subject to the terms and
    conditions of the Plastimatch Software License.
    See LICENSE file for the full Plastimatch Software License text.

    Copyright (c) 2026 MetaX Integrated Circuits (Shanghai) Co., Ltd. All rights reserved.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--num-angles", type=int, default=120)
    parser.add_argument("--angle-spacing", type=float, default=3.0)
    parser.add_argument("--sad", type=float, default=1000.0)
    parser.add_argument("--sid", type=float, default=1500.0)
    parser.add_argument("--dim", nargs=2, type=int, default=(128, 128), metavar=("NX", "NY"))
    parser.add_argument("--detector-size", nargs=2, type=float, default=(160.0, 160.0), metavar=("SX", "SY"))
    parser.add_argument("--threading", default="cpu")
    parser.add_argument(
        "--plastimatch",
        default=os.environ.get("PLASTIMATCH_BIN", "plastimatch"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = args.input.resolve()
    output_dir = args.output_dir.resolve()
    if not input_path.is_file():
        raise FileNotFoundError(input_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = output_dir / "proj_"
    command = [
        args.plastimatch,
        "drr",
        "--threading", args.threading,
        "--output-format", "pfm",
        "--num-angles", str(args.num_angles),
        "--gantry-angle-spacing", str(args.angle_spacing),
        "--sad", str(args.sad),
        "--sid", str(args.sid),
        "--dim", f"{args.dim[0]} {args.dim[1]}",
        "--detector-size", f"{args.detector_size[0]} {args.detector_size[1]}",
        "--input", str(input_path),
        "--output", str(prefix),
    ]
    log_path = output_dir / "drr.log"
    print("$", " ".join(command))
    with log_path.open("w", encoding="utf-8") as log:
        result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, text=True, check=False)
    if result.returncode != 0:
        tail = log_path.read_text(encoding="utf-8", errors="replace")[-4000:]
        raise RuntimeError(f"plastimatch drr failed ({result.returncode})\n{tail}")
    projections = sorted(output_dir.glob("proj_*.pfm"))
    geometry = sorted(output_dir.glob("proj_*.txt"))
    if len(projections) != args.num_angles or len(geometry) != args.num_angles:
        raise RuntimeError(
            f"expected {args.num_angles} PFM/TXT pairs, got {len(projections)}/{len(geometry)}"
        )
    if {path.stem for path in projections} != {path.stem for path in geometry}:
        raise RuntimeError("PFM and geometry basenames do not match")
    print(json.dumps({
        "task": "drr",
        "projections": len(projections),
        "output_dir": str(output_dir),
        "log": str(log_path),
    }, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
