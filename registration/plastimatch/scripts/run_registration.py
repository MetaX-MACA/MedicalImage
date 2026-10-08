#!/usr/bin/env python3
""" Run Plastimatch rigid + native B-spline registration.

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
    parser.add_argument("--fixed", type=Path, required=True)
    parser.add_argument("--moving", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--plastimatch",
        default=os.environ.get("PLASTIMATCH_BIN", "plastimatch"),
    )
    parser.add_argument("--gpuid", type=int, default=0)
    parser.add_argument("--max-its", type=int, default=50)
    parser.add_argument("--threading", default="cpu")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    fixed = args.fixed.resolve()
    moving = args.moving.resolve()
    output_dir = args.output_dir.resolve()
    if not fixed.is_file() or not moving.is_file():
        raise FileNotFoundError(f"fixed/moving input does not exist: {fixed}, {moving}")
    output_dir.mkdir(parents=True, exist_ok=True)

    warped = output_dir / "warped.mha"
    transform = output_dir / "transform.txt"
    internal_log = output_dir / "register-internal.log"
    config = output_dir / "register.txt"
    config.write_text(
        "\n".join(
            [
                "[GLOBAL]",
                f"fixed={fixed}",
                f"moving={moving}",
                f"img_out={warped}",
                f"xform_out={transform}",
                f"log={internal_log}",
                "",
                "[STAGE]",
                "xform=rigid",
                "impl=itk",
                "optim=versor",
                "metric=mse",
                "max_its=70",
                "",
                "[STAGE]",
                "xform=bspline",
                "impl=plastimatch",
                "optim=lbfgsb",
                "metric=mse",
                # The registration command file names the CPU backend
                # ``openmp`` (the CLI drr/fdk commands use ``cpu``).
                f"threading={'openmp' if args.threading == 'cpu' else args.threading}",
                f"gpuid={args.gpuid}",
                f"max_its={args.max_its}",
                "grid_spac=24 24 24",
                "res=2 2 2",
                "",
            ]
        ),
        encoding="utf-8",
    )
    log_path = output_dir / "register.log"
    command = [args.plastimatch, "register", str(config)]
    print("$", " ".join(command))
    with log_path.open("w", encoding="utf-8") as log:
        result = subprocess.run(
            command,
            stdout=log,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
    if result.returncode != 0:
        tail = log_path.read_text(encoding="utf-8", errors="replace")[-4000:]
        raise RuntimeError(f"plastimatch register failed ({result.returncode})\n{tail}")
    missing = [str(path) for path in (warped, transform) if not path.is_file()]
    if missing:
        raise RuntimeError("registration completed without expected files: " + ", ".join(missing))
    print(json.dumps({
        "task": "registration",
        "warped": str(warped),
        "transform": str(transform),
        "log": str(log_path),
    }, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
