import gdsfactory as gf

gf.clear_cache()


import gfelib as gl

import sys
import datetime
import argparse

from pdk import LAYERS, PDK
from device import (
    RFLEX_PROTECTION_ISOLATION,
    device,
    CHIP_SIZE,
    CAVITY_WIDTH,
    DEVICE_MIN_ISOLATION,
)

DEVICE_CD_COMPENSATION_DEFAULT = 0.3
HANDLE_CD_COMPENSATION_DEFAULT = 0

# Isolation distance for device layers
DEVICE_MERGING_ISOLATION = [
    DEVICE_MIN_ISOLATION,  # P0
    DEVICE_MIN_ISOLATION,  # P1
    RFLEX_PROTECTION_ISOLATION,  # P2
    DEVICE_MIN_ISOLATION,  # P3
    DEVICE_MIN_ISOLATION,  # P4
    DEVICE_MIN_ISOLATION,  # P5
    DEVICE_MIN_ISOLATION,  # P6
    DEVICE_MIN_ISOLATION,  # P7
]

HANDLE_MERGING_ISOLATION = CAVITY_WIDTH

# Layers for generating reticle/masks
reticle_layers = {
    LAYERS.TIP: {"mirror": False, "type": "stepper"},
    LAYERS.DEVICE_REMOVE: {"mirror": False, "type": "stepper"},
    LAYERS.VIAS_ETCH: {"mirror": False, "type": "stepper"},
    LAYERS.HANDLE_STEP_ETCH: {"mirror": True, "type": "stepper"},
    LAYERS.HANDLE_REMOVE: {"mirror": True, "type": "wafer"},
}

PDK.activate()

import gfebuild as gb

parser = argparse.ArgumentParser(description="Build script for MEGA-2D")
parser.add_argument(
    "--no-merge",
    action="store_true",
    help="Don't merge the device patterns (e.g. release holes), because it can be very slow. For debug use only, ASML reticle files will not be generated",
)
# parser.add_argument(
#     "--mirror",
#     action="store_true",
#     help="Write additional ASML reticle files that are mirrored across x=0 (PLACEMENTS file is not mirrored)",
# )
parser.add_argument(
    "--show",
    action="store_true",
    help="Show the last pattern with KLayout",
)
parser.add_argument(
    "--version",
    action="store",
    type=str,
    help="Add version number text",
    required=True,
)
parser.add_argument(
    "--hash",
    action="store",
    type=str,
    help="Add hash text",
    default="",
)
parser.add_argument(
    "--comp-handle",
    action="store",
    type=float,
    help="Compensate handle (+ is expand)",
    default=HANDLE_CD_COMPENSATION_DEFAULT,
)
parser.add_argument(
    "--comp-device",
    action="store",
    type=float,
    help="Compensate device (+ is expand)",
    default=DEVICE_CD_COMPENSATION_DEFAULT,
)

args = parser.parse_args()

date_str = str(datetime.date.today())

filename_prefix = f"mega_2d_{args.version}_{args.hash[:7]}_{date_str}"

WAFER_DIAMETER = 150000
# WAFER_ALIGNMENT_MARKS = [
#     (-40000, 2000),
#     (40000, 2000),
#     (-40000, -2000),
#     (40000, -2000),
#     (-8000, 48000),
#     (8000, 48000),
# ]

CHIP_RECT = gf.components.rectangle(
    size=(CHIP_SIZE, CHIP_SIZE),
    layer=LAYERS.DUMMY,
    centered=True,
)

d = device(ver=f"Ver {args.version}\n{args.hash[:7]}\n{date_str}")

d.write_gds(f"./build/{filename_prefix}_SOURCE.gds")

c = gf.Component(name="chip")

# DEVICE_Px isolation
dev = gf.Component()

for i in range(7, -1, -1):
    dev = gf.boolean(
        A=dev,
        B=d,
        operation="|",
        layer=LAYERS.DEVICE,
        layer1=LAYERS.DEVICE,
        layer2=(LAYERS.DEVICE_P0[0], i),
    )

    exp = gf.boolean(
        A=gf.Component(),
        B=d,
        operation="|",
        layer=LAYERS.DUMMY,
        layer1=LAYERS.DUMMY,
        layer2=(LAYERS.DEVICE_P0[0], i),
    )
    exp.offset(layer=LAYERS.DUMMY, distance=DEVICE_MERGING_ISOLATION[i])

    iso = gf.boolean(
        A=exp,
        B=d,
        operation="-",
        layer=LAYERS.DUMMY,
        layer1=LAYERS.DUMMY,
        layer2=(LAYERS.DEVICE_P0[0], i),
    )

    dev = gf.boolean(
        A=dev,
        B=iso,
        operation="-",
        layer=LAYERS.DEVICE,
        layer1=LAYERS.DEVICE,
        layer2=LAYERS.DUMMY,
    )

    # Merge NoISO layer
    dev = gf.boolean(
        A=dev,
        B=d,
        operation="|",
        layer=LAYERS.DEVICE,
        layer1=LAYERS.DEVICE,
        layer2=(LAYERS.DEVICE_P0[0], i + 10),
    )

# Pattern in layer DEVICE is always present in final design
dev = gf.boolean(
    A=dev,
    B=d,
    operation="|",
    layer=LAYERS.DEVICE,
    layer1=LAYERS.DEVICE,
    layer2=LAYERS.DEVICE,
)

if not args.no_merge:
    # DEVICE merged
    _ = c << gf.boolean(
        A=gf.boolean(
            A=CHIP_RECT,
            B=dev,
            operation="-",
            layer=LAYERS.DUMMY,
            layer1=LAYERS.DUMMY,
            layer2=LAYERS.DEVICE,
        ),
        B=d,
        operation="|",
        layer=LAYERS.DEVICE_REMOVE,
        layer1=LAYERS.DUMMY,
        layer2=LAYERS.DEVICE_REMOVE,
    )
else:
    # DEVICE and DEVICE_REMOVE not merged
    c << dev
    c << d.extract(layers=[LAYERS.DEVICE_REMOVE])

# HANDLE
handle = gf.Component()

for i in range(7, -1, -1):
    handle = gf.boolean(
        A=handle,
        B=d,
        operation="-",
        layer=LAYERS.DUMMY,
        layer1=LAYERS.DUMMY,
        layer2=(LAYERS.HANDLE_P0[0], i),
    )

    exp = gf.boolean(
        A=gf.Component(),
        B=d,
        operation="|",
        layer=LAYERS.DUMMY,
        layer1=LAYERS.DUMMY,
        layer2=(LAYERS.HANDLE_P0[0], i),
    )
    exp.offset(layer=LAYERS.DUMMY, distance=HANDLE_MERGING_ISOLATION)

    border = gf.boolean(
        A=exp,
        B=d,
        operation="-",
        layer=LAYERS.DUMMY,
        layer1=LAYERS.DUMMY,
        layer2=(LAYERS.HANDLE_P0[0], i),
    )

    handle = gf.boolean(
        A=handle,
        B=border,
        operation="|",
        layer=LAYERS.DUMMY,
        layer1=LAYERS.DUMMY,
        layer2=LAYERS.DUMMY,
    )

_ = c << gf.boolean(
    A=handle,
    B=d,
    operation="|",
    layer=LAYERS.HANDLE_REMOVE,
    layer1=LAYERS.DUMMY,
    layer2=LAYERS.HANDLE_REMOVE,
)

# HANDLE_STEP_ETCH (must expose all HANDLE_REMOVE feature as well)
_ = c << gf.boolean(
    A=c,
    B=d,
    operation="|",
    layer=LAYERS.HANDLE_STEP_ETCH,
    layer1=LAYERS.HANDLE_REMOVE,
    layer2=LAYERS.HANDLE_STEP_ETCH,
)


# POSITIVE LAYERS
for layer in [
    LAYERS.VIAS_ETCH,
    LAYERS.TIP0,
]:
    _ = c << gf.boolean(
        A=CHIP_RECT,
        B=d,
        operation="&",
        layer=layer,
        layer1=LAYERS.DUMMY,
        layer2=layer,
    )

# NEGATIVE LAYERS
for layer in []:
    _ = c << gf.boolean(
        A=CHIP_RECT,
        B=d,
        operation="-",
        layer=layer,
        layer1=LAYERS.DUMMY,
        layer2=layer,
    )

# PROCESS COMPENSATION

# Add CD compensation
c.offset(layer=LAYERS.DEVICE, distance=args.comp_device)
c.offset(layer=LAYERS.DEVICE_REMOVE, distance=-args.comp_device)
c.offset(layer=LAYERS.HANDLE_REMOVE, distance=-args.comp_handle)

c.flatten()
c.write_gds(
    f"./build/{filename_prefix}_BUILD.gds",
    with_metadata=False,
)

if not args.no_merge:

    stepper_layers = [
        layer for layer, spec in reticle_layers.items() if spec["type"] == "stepper"
    ]
    wafer_layers = [
        layer for layer, spec in reticle_layers.items() if spec["type"] == "wafer"
    ]

    # generate stepper reticles
    r = c.copy()

    # Mirror the specified layers
    for layer in stepper_layers:
        if reticle_layers[layer]["mirror"]:
            r.remove_layers([layer])
            r << (c.extract([layer]).mirror_x())

    reticles, placements = gb.asml300.reticle(
        component=r,
        image_size=(CHIP_SIZE, CHIP_SIZE),
        image_layers=stepper_layers,
        id=f"M2D-{args.version}",
        text=date_str,
    )

    for i, reticle in enumerate(reticles):
        for layer, pos in placements.items():
            if pos[0] == i:
                _ = reticle << gf.components.text(
                    text=str(LAYERS(layer))
                    + (" (mirror)" if reticle_layers[layer]["mirror"] else ""),
                    size=0.2 * CHIP_SIZE,
                    position=(pos[1], pos[2]),
                    justify="center",
                    layer=LAYERS.DUMMY,
                )
        reticle.flatten()
        reticle.write_gds(
            f"./build/{filename_prefix}_RETICLE_ASML_{i}.gds", with_metadata=False
        )

    with open(f"./build/{filename_prefix}_RETICLE_ASML_PLACEMENTS.txt", "w") as f:
        for layer, pos in placements.items():
            f.write(f"{LAYERS(layer)}: {pos[0]}, {pos[1]:.2f}, {pos[2]:.2f}\n")

# generate wafer masks for backside
# for layer in [LAYERS.HANDLE_REMOVE, LAYERS.CAP_BACKSIDE]:
#     wafer, placements = gb.asml300.wafer(
#         radius=0.5 * WAFER_DIAMETER,
#         chip_center=True,
#         place_partial=False,
#         marks=WAFER_ALIGNMENT_MARKS,
#         component=c,
#         image_size=(CHIP_SIZE, CHIP_SIZE),
#         image_layer=layer,
#         id=f"MPC-{args.version}-{LAYERS(layer)}",
#         text=date_str,
#     )
#     wafer.write_gds(
#         f"./build/mega_pc_{args.version}_BUILD_WAFER_{LAYERS(layer)}.gds",
#         with_metadata=False,
#     )

#     if args.mirror:
#         wafer.mirror_x(0)
#         wafer.write_gds(
#             f"./build/mega_pc_{args.version}_BUILD_WAFER_{LAYERS(layer)}_MIRROR.gds",
#             with_metadata=False,
#         )

#     with open(
#         f"./build/mega_pc_{args.version}_BUILD_WAFER_{LAYERS(layer)}_PLACEMENTS.txt",
#         "w",
#     ) as f:
#         f.write(f"WAFER_DIAMETER: {WAFER_DIAMETER:.2f}\n")
#         f.write(f"X_STEP_SIZE: {CHIP_SIZE:.2f}\n")
#         f.write(f"Y_STEP_SIZE: {CHIP_SIZE:.2f}\n")
#         f.write(f"CHIP_COUNT: {len(placements)}\n")
#         f.write(f"\n")
#         for mark in WAFER_ALIGNMENT_MARKS:
#             f.write(f"MARK: {mark[0]:.2f}, {mark[1]:.2f}\n")
#         f.write(f"\n")
#         for placement in placements:
#             f.write(f"CHIP: {placement[0]:.2f}, {placement[1]:.2f}\n")


if args.show:
    c.show()
