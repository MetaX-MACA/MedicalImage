#!/usr/bin/env python3
""" Reconstruct a volume from a Plastimatch DRR directory with FDK.

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
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--image-range", nargs=2, type=int, metavar=("FIRST", "LAST"))
    parser.add_argument("--dim", nargs=3, type=int, default=(128, 128, 128), metavar=("NX", "NY", "NZ"))
    parser.add_argument("--volume-size", nargs=3, type=float, default=(128.0, 128.0, 128.0), metavar=("SX", "SY", "SZ"))
    parser.add_argument("--filter", default="ramp")
    parser.add_argument("--threading", default="cpu")
    parser.add_argument(
        "--plastimatch",
        default=os.environ.get("PLASTIMATCH_BIN", "plastimatch"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_dir = args.input_dir.resolve()
    output_path = args.output.resolve()
    if not input_dir.is_dir():
        raise NotADirectoryError(input_dir)
    projections = sorted(input_dir.glob("proj_*.pfm"))
    if not projections:
        raise RuntimeError(f"no proj_*.pfm files found in {input_dir}")
    image_range = args.image_range or (0, len(projections) - 1)
    if image_range[0] < 0 or image_range[1] < image_range[0]:
        raise ValueError(f"invalid image range: {image_range}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        args.plastimatch,
        "fdk",
        "--threading", args.threading,
        "--filter", args.filter,
        "--image-range", f"{image_range[0]} {image_range[1]}",
        "--dim", " ".join(map(str, args.dim)),
        "--volume-size", " ".join(map(str, args.volume_size)),
        "--input", str(input_dir),
        "--output", str(output_path),
    ]
    log_path = output_path.parent / "fdk.log"
    print("$", " ".join(command))
    with log_path.open("w", encoding="utf-8") as log:
        result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, text=True, check=False)
    if result.returncode != 0:
        tail = log_path.read_text(encoding="utf-8", errors="replace")[-4000:]
        raise RuntimeError(f"plastimatch fdk failed ({result.returncode})\n{tail}")
    if not output_path.is_file():
        raise RuntimeError(f"FDK exited successfully but did not create {output_path}")
    print(json.dumps({
        "task": "fdk",
        "reconstruction": str(output_path),
        "input_projections": len(projections),
        "log": str(log_path),
    }, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
