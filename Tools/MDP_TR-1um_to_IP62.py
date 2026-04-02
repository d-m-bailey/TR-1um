#!/usr/bin/env python3
# ----- ------ ----- ----- ------ ----- ----- ------ -----
# Copyright (c) 2026 jun1okamura
# SPDX-License-Identifier: Apache-2.0
# ----- ------ ----- ----- ------ ----- ----- ------ -----

import sys
import subprocess
import shutil
import click

KLAYOUT_BIN = shutil.which("klayout") or "/usr/local/bin/klayout"

@click.command()
@click.argument(
    "rfile",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.argument(
    "input_gds",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.argument(
    "output_gds",
    type=click.Path(file_okay=True, dir_okay=False),
)
@click.option("--top", required=True, help="Top cell name")
def mdp(rfile: str, input_gds: str, output_gds: str, top: str):

    cmd = [
        KLAYOUT_BIN,
        "-b",
        "-r", rfile,
        "-rd", f"cellname={top}",
        "-rd", f"input={input_gds}",
        "-rd", f"output={output_gds}",
    ]

    print("Running:", " ".join(cmd))

    result = subprocess.run(cmd, capture_output=True, text=True)

    print(result.stdout)

    if result.returncode != 0:
        print("ERROR:")
        print(result.stderr)
        sys.exit(result.returncode)

    print("Done.")


if __name__ == "__main__":
    mdp()