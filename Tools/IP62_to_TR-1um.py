#!/usr/bin/env python3
# ----- ------ ----- ----- ------ ----- ----- ------ -----
# TR-1um DRC / IP62 to TR-1um converter
# Original version was made by jun1okamura from TokaiRika's document
# LICENSE: Apache License Version 2.0, January 2004
#          http://www.apache.org/licenses/
# ----- ------ ----- ----- ------ ----- ----- ------ -----
#
# Usage:
#   python3 IP62_to_TR-1um.py INPUT_IP62_GDS OUTPUT_TR-1um_GDS
#

from __future__ import annotations

import argparse
from pathlib import Path

import klayout.db as db


FLATTEN_CELL_PREFIXES = [
    "DCONT",
    "pcont",
    "MNE_CDNS",
    "MPE_CDNS",
    "BGMN_CDNS",
    "BGMP_CDNS",
    "VIA_M21",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert IP62 GDS layers into TR-1um drawing layers."
    )
    parser.add_argument("input_gds", type=Path, help="Input IP62 GDS file")
    parser.add_argument("output_gds", type=Path, help="Output TR-1um GDS file")
    return parser.parse_args()


def region(cell: db.Cell, layer_index: int) -> db.Region:
    return db.Region(cell.shapes(layer_index)).merged()


def starts_with_any(name: str, prefixes: list[str]) -> bool:
    return any(name.startswith(prefix) for prefix in prefixes)


def define_layers(layout: db.Layout) -> dict[str, int]:
    layers: dict[str, int] = {}

    # IP62 layers
    layers["PSUB"] = layout.layer(140, 0)
    layers["NW"] = layout.layer(36, 0)
    layers["HVNW"] = layout.layer(141, 0)
    layers["L"] = layout.layer(3, 0)
    layers["NF"] = layout.layer(25, 0)
    layers["PF"] = layout.layer(26, 0)
    layers["HPBE"] = layout.layer(144, 0)
    layers["HNBE"] = layout.layer(145, 0)
    layers["PBE"] = layout.layer(146, 0)
    layers["NBE"] = layout.layer(147, 0)
    layers["SG"] = layout.layer(8, 0)
    layers["PM"] = layout.layer(35, 0)
    layers["NM"] = layout.layer(7, 0)
    layers["PSD"] = layout.layer(9, 0)
    layers["NSD"] = layout.layer(28, 0)
    layers["R"] = layout.layer(12, 0)
    layers["CL"] = layout.layer(143, 0)
    layers["HPM"] = layout.layer(33, 0)
    layers["ESD"] = layout.layer(63, 2)

    # DLXXX layers
    layers["DPBG"] = layout.layer(116, 0)
    layers["DNBG"] = layout.layer(117, 0)
    layers["DRBG"] = layout.layer(118, 0)
    layers["DCBG"] = layout.layer(119, 0)
    layers["DLWLMP"] = layout.layer(150, 0)
    layers["DLWLMN"] = layout.layer(151, 0)
    layers["DLWLRR"] = layout.layer(154, 0)
    layers["DLMP"] = layout.layer(157, 0)
    layers["DLMN"] = layout.layer(158, 0)
    layers["DLRR"] = layout.layer(162, 0)
    layers["DLRS"] = layout.layer(165, 0)
    layers["DLCSIO"] = layout.layer(166, 0)
    layers["DLDP"] = layout.layer(167, 0)
    layers["DLDN"] = layout.layer(168, 0)
    layers["DLMPE"] = layout.layer(169, 0)
    layers["DLMNE"] = layout.layer(170, 0)
    layers["DLBGMP"] = layout.layer(177, 0)
    layers["DLBGMN"] = layout.layer(178, 0)
    layers["DLBGRR"] = layout.layer(182, 0)

    # Drawing layers
    layers["AP"] = layout.layer(3, 1)
    layers["AN"] = layout.layer(3, 2)
    layers["AR"] = layout.layer(3, 3)
    layers["AC"] = layout.layer(3, 4)
    layers["GC"] = layout.layer(8, 1)
    layers["GR"] = layout.layer(8, 2)

    return layers


def convert_flatten(layout: db.Layout, cell: db.Cell) -> None:
    if starts_with_any(cell.name, FLATTEN_CELL_PREFIXES):
        return

    for inst in cell.each_inst():
        child = layout.cell(inst.cell_index)
        if child is None:
            continue

        if starts_with_any(child.name, FLATTEN_CELL_PREFIXES):
            print(f"Flatten CELL in {cell.name:<20} : {child.name:<20}")
            inst.flatten(0)


def delete_flatten(cell: db.Cell) -> None:
    if starts_with_any(cell.name, FLATTEN_CELL_PREFIXES):
        print(f"DELETE: {cell.name}")
        cell.delete()


def should_skip_cell(cell: db.Cell) -> bool:
    name_parts = cell.name.split("_")

    if len(name_parts) > 2:
        if name_parts[0] == "chip" and name_parts[1] == "outline" and name_parts[2] == "462":
            return True
        if name_parts[0] == "OSS" and name_parts[1] == "EDGE":
            return True

    return False


def insert_region_as_polygons(cell: db.Cell, layer_index: int, reg: db.Region) -> None:
    for shape in reg:
        cell.shapes(layer_index).insert(db.Polygon(shape))


def clear_layers(cell: db.Cell, layer_indexes: list[int]) -> None:
    for layer_index in layer_indexes:
        cell.shapes(layer_index).clear()


def convert_drawing(cell: db.Cell, layers: dict[str, int]) -> None:
    psub = region(cell, layers["PSUB"])
    nw = region(cell, layers["NW"])
    hvnw = region(cell, layers["HVNW"])
    poly = region(cell, layers["L"])
    sg = region(cell, layers["SG"])
    psd = region(cell, layers["PSD"])
    nsd = region(cell, layers["NSD"])
    res = region(cell, layers["R"])
    cl = region(cell, layers["CL"])

    dlmp = region(cell, layers["DLMP"])
    dlmn = region(cell, layers["DLMN"])
    dlmpe = region(cell, layers["DLMPE"])
    dlmne = region(cell, layers["DLMNE"])
    dldp = region(cell, layers["DLDP"])
    dldn = region(cell, layers["DLDN"])
    dlbgmp = region(cell, layers["DLBGMP"])
    dlbgmn = region(cell, layers["DLBGMN"])
    dlrr = region(cell, layers["DLRR"])
    dlbgrr = region(cell, layers["DLBGRR"])
    dlcsio = region(cell, layers["DLCSIO"])
    dlrs = region(cell, layers["DLRS"])

    nwmp = (psub & nw).not_interacting(cl)
    nwcs = (psub & nw.interacting(cl))
    nwrr = psub & hvnw
    pwmn = db.Region(cell.bbox()) - psub

    lg = poly.interacting(sg)
    lx = poly.not_interacting(sg)

    p1 = sg - dlrs
    p2 = sg & dlrs

    l7 = psd
    l8 = nsd
    l9 = res
    la = cl

    aamp = (lg & (nwmp - l7 & l8 - l9 - la)) | (lg & dlmp)
    aamn = (lg & (pwmn & l7 - l8 - l9 - la)) | (lg & dlmn)
    aape = (lg & (nwmp - l7 & l8 - l9 - la)) | (lg & dlmpe)
    aane = (lg & (pwmn & l7 - l8 - l9 - la)) | (lg & dlmne)

    aadp = (lx & (nwmp - l7 & l8 - l9 - la)) | (lx & dldp)
    aadn = (lx & (pwmn & l7 - l8 - l9 - la)) | (lx & dldn)
    aagp = (lx & (nwmp & l7 - l8 - l9 - la)) | (lx & dlbgmp)
    aagn = (lx & (pwmn - l7 & l8 - l9 - la)) | (lx & dlbgmn)

    aarr = (lx & (nwrr & l8 & l9 - la)) | (lx & dlrr)
    aagr = (lx & (nwrr & l7 - l8 - l9 - la)) | (lx & dlbgrr)
    aacc = (lg & (nwcs & l7 & l8 - l9 & la)) | (lg & nwcs & dlcsio)
    aagc = (lx & (nwcs & l7 - l8 - l9 - la)) | (lx & nwcs & dlbgmn)

    insert_region_as_polygons(cell, layers["AP"], aamp + aape + aagn + aadp)
    insert_region_as_polygons(cell, layers["AN"], aamn + aane + aagp + aadn + aagr + aagc)
    insert_region_as_polygons(cell, layers["AR"], aarr)
    insert_region_as_polygons(cell, layers["AC"], aacc)
    insert_region_as_polygons(cell, layers["GC"], p1)
    insert_region_as_polygons(cell, layers["GR"], p2)

    clear_layers(
        cell,
        [
            layers["NW"],
            layers["HVNW"],
            layers["L"],
            layers["NF"],
            layers["PF"],
            layers["HPBE"],
            layers["HNBE"],
            layers["PBE"],
            layers["NBE"],
            layers["PM"],
            layers["NM"],
            layers["SG"],
            layers["PSD"],
            layers["NSD"],
            layers["R"],
            layers["CL"],
            layers["HPM"],
        ],
    )

    clear_layers(
        cell,
        [
            layers["DPBG"],
            layers["DNBG"],
            layers["DRBG"],
            layers["DCBG"],
            layers["DLWLMP"],
            layers["DLWLMN"],
            layers["DLWLRR"],
            layers["DLMP"],
            layers["DLMN"],
            layers["DLRR"],
            layers["DLRS"],
            layers["DLCSIO"],
            layers["DLDP"],
            layers["DLDN"],
            layers["DLMPE"],
            layers["DLMNE"],
            layers["DLBGMP"],
            layers["DLBGMN"],
            layers["DLBGRR"],
        ],
    )


def main() -> None:
    args = parse_args()

    layout = db.Layout()
    layout.read(str(args.input_gds))

    layers = define_layers(layout)

    for cell in layout.each_cell():
        convert_flatten(layout, cell)

    for index in layout.each_cell_bottom_up():
        cell = layout.cell(index)
        if cell is None:
            continue

        if should_skip_cell(cell):
            print(f"CELL({index:2d}): {cell.name}")
            continue

        convert_drawing(cell, layers)

    for cell in layout.each_cell():
        if cell.destroyed():
            continue
        delete_flatten(cell)

    layout.write(str(args.output_gds))


if __name__ == "__main__":
    main()