import gdsfactory as gf
import gfelib as gl
import klayout

import numpy as np
import functools

from pdk import LAYERS, PDK

PDK.activate()

static_cell = functools.partial(gf.cell, check_instances=False)

# GLOBAL CONSTANTS
CHIP_SIZE = 6000
CHIP_BORDER_WIDTH = 200

ANGLE_RESOLUTION = 0.5
CAVITY_WIDTH = 50
DEVICE_ISOLATION = 5
ELEC_ROUTING_WIDTH = 50

RELEASE_SPEC = gl.datatypes.ReleaseSpec(
    hole_radius=3,
    distance=6,
    angle_resolution=18,
    layer=LAYERS.DEVICE_REMOVE,
)

CENTER_CARRIAGE_RADIUS = 75
# CENTER_CARRIAGE_CAVITY_RADIUS = 250

TIP_SIZE = 4
TIP_GUARD_RING_RADIUSES = [CENTER_CARRIAGE_RADIUS + CAVITY_WIDTH * 2, 500]
TIP_GUARD_RING_THICKNESS = 5

RFLEX_INNER_RADIUS0 = 90
RFLEX_INNER_RADIUS1 = 110
RFLEX_ANCHOR_RADIUS0 = 670
RFLEX_ANCHOR_RADIUS1 = 740
RFLEX_BEAM_WIDTH = 2.4
RFLEX_BEAM_SPEC = gl.datatypes.BeamSpec(
    release_thick=True,
    thick_length=(0, 0.7),
    thick_width=(20, 0),
    thick_offset=(0, 0),
)
RFLEX_BEAM_ANGLES = [30, 60]

RDRIVE_INNER_RADIUS = 950
RDRIVE_MID_RADIUS = 1000
RDRIVE_OUTER_RADIUS = 1100
RDRIVE_TEETH_PITCH = 2 / 3
RDRIVE_TEETH_WIDTH = 4
RDRIVE_TEETH_HEIGHT = 7
RDRIVE_TEETH_CLEARANCE = 1.6
RDRIVE_TEETH_PHASE = [-120, 0, 120]
RDRIVE_PHASE_SPAN = 40
RDRIVE_TEETH_COUNT = int(np.floor(RDRIVE_PHASE_SPAN / RDRIVE_TEETH_PITCH))
RDRIVE_ROTOR_SPAN = 150
RDRIVE_STATOR_SPAN_MIN = RDRIVE_PHASE_SPAN * len(RDRIVE_TEETH_PHASE)
RDRIVE_ANCHOR_BASE_SPAN = 20

RSENSOR_START_ANGLE = 40
RSENSOR_END_ANGLE = 89
RSENSOR_COMB_GAP = 5
RSENSOR_COMB_WIDTH = 6
RSENSOR_COMB_COUNT = int(
    np.floor(
        (RDRIVE_INNER_RADIUS - RFLEX_ANCHOR_RADIUS1 - RSENSOR_COMB_WIDTH)
        / (RSENSOR_COMB_GAP + RSENSOR_COMB_WIDTH)
    )
)
RSENSOR_COMB_OVERLAP = 19

R_CONNECTOR_CLEARANCE = 10  # Mechanical clearance
R_CONNECTOR_ISOLATION = 5  # Electrical isolatioin distance

RSTOPPER_ANGLE = 45
RSTOPPER_SPAN = 3
RSTOPPER_LENGTH = 25

RANCHOR_ANGLE = RFLEX_BEAM_ANGLES[0] + 0.5 * RFLEX_BEAM_WIDTH / RFLEX_ANCHOR_RADIUS0 / (
    np.pi / 180
)

# ZDRIVE_CLEARANCE = 8
# ZDRIVE_INNER_RADIUS = 2250
ZDRIVE_OUTER_RADIUS = 1280
# ZDRIVE_RING_SPAN = 60
# ZDRIVE_ANCHOR_SIZE = 120

Z_RELEASE_LOCK_SPAN = (40, 50)

ZCANT_WIDTH = 600
ZCANT_LENGTH1 = 600
ZCANT_LENGTH2 = 100
ZCANT_BEAM0_WIDTH = 5
ZCANT_BEAM0_LENGTH = 100
ZCANT_BEAM1_WIDTH = 5
ZCANT_BEAM1_LENGTH = 100
ZCANT_BEAM2_WIDTH = 4
ZCANT_BEAM2_LENGTH = 150
ZCANT_BEAM2_INSET = 230
ZCANT_STUB_WIDTH = 40
ZCANT_STUB_INSET = 70
ZCANT_STUB_ANCHOR_SIZE = 250

Z_CANT_BEAM_SPEC = None

ZACTUATOR_WIDTH = 2800
ZACTUATOR_LENGTH = 700
ZACTUATOR_LENGTH_STEP = 5
ZACTUATOR_BEAM_WIDTH = 4
ZACTUATOR_BEAM_LENGTH = 40

ZR_CONNECTOR_SPANS = [
    (-30, -25),
    (15, 20),
    (60, 65),
]

WIRE_BOND_SIZE = 300
WIRE_BOND_OFFSET = 100

# CHIP_BOND_RADIUS = 2600
# CHIP_BOND_SPAN = 60
# CHIP_BOND_MARKER_SIZE = 100


VIA_RADIUS = 20
VIA_DEVICE_CLEARANCE = DEVICE_ISOLATION
VIA_HANDLE_CLEARANCE = 30
VIA_VIA_CLEARANCE = 75

via = lambda layer: gl.basic.via(
    radius_first=VIA_RADIUS,
    radius_last=VIA_RADIUS + VIA_DEVICE_CLEARANCE,
    geometry_layers=[
        LAYERS.VIAS_ETCH,
        layer,
    ],
    angle_resolution=ANGLE_RESOLUTION,
)


@static_cell
def chip_border() -> gf.Component:
    c = gf.Component()
    _ = c << gl.device.chip_border(
        size=(CHIP_SIZE, CHIP_SIZE),
        width=CHIP_BORDER_WIDTH,
        geometry_layer=LAYERS.DEVICE_P3,
        handle_layer=LAYERS.HANDLE_P7,
        centered=True,
        release_spec=RELEASE_SPEC,
    )

    # pos = 2 * WIRE_BOND_SIZE + WIRE_BOND_OFFSET + CAVITY_WIDTH
    # size = 0.5 * CHIP_SIZE - CHIP_BORDER_WIDTH - pos - CAVITY_WIDTH
    # for r in [0, 90, 180, 270]:
    #     ref = c << gf.components.rectangle(
    #         size=(size, size),
    #         layer=LAYERS.DEVICE,
    #         centered=False,
    #     )
    #     ref.move((pos, pos))
    #     ref.rotate(angle=r, center=(0, 0))

    return c


@static_cell
def center_carriage() -> gf.Component:
    c = gf.Component()

    _ = c << gf.components.circle(
        radius=CENTER_CARRIAGE_RADIUS,
        angle_resolution=ANGLE_RESOLUTION,
        layer=LAYERS.DEVICE_P3,
    )

    _ = c << gf.components.circle(
        radius=CENTER_CARRIAGE_RADIUS,
        angle_resolution=ANGLE_RESOLUTION,
        layer=LAYERS.HANDLE_P1,
    )

    _ = c << gf.components.rectangle(
        size=(TIP_SIZE, TIP_SIZE),
        centered=True,
        layer=LAYERS.TIP,
    )

    for radius in TIP_GUARD_RING_RADIUSES:
        _ = c << gf.components.ring(
            radius=radius,
            width=TIP_GUARD_RING_THICKNESS,
            layer=LAYERS.TIP,
            angle=360,
        )

    _ = c << via(LAYERS.DEVICE_P3)

    return c


@static_cell
def r_flexure_full() -> gf.Component:
    c = gf.Component()

    butt: gf.Component = gl.flexure.butterfly(
        radius0=RFLEX_INNER_RADIUS0,
        radius1=RFLEX_INNER_RADIUS1,
        radius2=RFLEX_ANCHOR_RADIUS0,
        width_beam=RFLEX_BEAM_WIDTH,
        angles=RFLEX_BEAM_ANGLES,
        release_inner=False,
        geometry_layer=LAYERS.DEVICE_P3,
        angle_resolution=ANGLE_RESOLUTION,
        beam_spec=RFLEX_BEAM_SPEC,
        release_spec=RELEASE_SPEC,
    )

    (c << butt).rotate(90)
    (c << butt).rotate(270)

    anchor_dev: gf.Component = gl.basic.ring(
        radius_inner=RFLEX_ANCHOR_RADIUS0,
        radius_outer=RFLEX_ANCHOR_RADIUS1,
        angles=(90 - RANCHOR_ANGLE, 90 + RANCHOR_ANGLE),
        geometry_layer=LAYERS.DEVICE_P3,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )

    anchor_dev_expand: gf.Component = gl.basic.ring(
        radius_inner=RFLEX_ANCHOR_RADIUS0,
        radius_outer=RFLEX_ANCHOR_RADIUS1 + R_CONNECTOR_CLEARANCE,
        angles=(90 - RANCHOR_ANGLE, 90 + RANCHOR_ANGLE),
        geometry_layer=LAYERS.DEVICE_P3,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )

    anchor_handle: gf.Component = gl.basic.ring(
        radius_inner=RFLEX_ANCHOR_RADIUS0,
        radius_outer=RFLEX_ANCHOR_RADIUS1,
        angles=(90 - RANCHOR_ANGLE, 90 + RANCHOR_ANGLE),
        geometry_layer=LAYERS.HANDLE_P1,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )

    for angle in [0, 90, 180, 270]:
        if angle in [0, 180]:
            (c << anchor_dev).rotate(angle, (0, 0))
        else:
            (c << anchor_dev_expand).rotate(angle, (0, 0))
        (c << anchor_handle).rotate(angle, (0, 0))

    return c


@static_cell
def r_drive_half() -> gf.Component:
    c = gf.Component()

    _ = c << gl.actuator.rotator_gear(
        radius_inner=RDRIVE_INNER_RADIUS,
        radius_gap=RDRIVE_MID_RADIUS,
        radius_outer=RDRIVE_OUTER_RADIUS,
        teeth_pitch=RDRIVE_TEETH_PITCH,
        teeth_width=RDRIVE_TEETH_WIDTH,
        teeth_height=RDRIVE_TEETH_HEIGHT,
        teeth_clearance=RDRIVE_TEETH_CLEARANCE,
        teeth_phase=RDRIVE_TEETH_PHASE,
        teeth_count=RDRIVE_TEETH_COUNT,
        inner_rotor=True,
        rotor_span=RDRIVE_ROTOR_SPAN,
        geometry_layer=LAYERS.DEVICE_P3,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=RELEASE_SPEC,
    )
    return c


@static_cell
def r_connectors_half() -> gf.Component:
    c = gf.Component()

    beam_angle = 90 - RFLEX_BEAM_ANGLES[1]
    connector0_angle = beam_angle + 0.5 * RFLEX_BEAM_WIDTH / RFLEX_ANCHOR_RADIUS1 / (
        np.pi / 180
    )
    connector1_angle = 0.5 * beam_angle

    # Inner connection (hollow part + solid part)
    _ = c << gl.basic.ring(
        radius_inner=CENTER_CARRIAGE_RADIUS
        - gl.utils.sagitta_offset_safe(
            radius=CENTER_CARRIAGE_RADIUS,
            chord=0,
            angle_resolution=ANGLE_RESOLUTION,
        ),
        radius_outer=RFLEX_ANCHOR_RADIUS0 - R_CONNECTOR_CLEARANCE,
        angles=(-connector1_angle, connector1_angle),
        geometry_layer=LAYERS.DEVICE_P3,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=RELEASE_SPEC,
    )

    _ = c << gl.basic.ring(
        radius_inner=RFLEX_ANCHOR_RADIUS0 - R_CONNECTOR_CLEARANCE,
        radius_outer=RFLEX_ANCHOR_RADIUS0
        + gl.utils.sagitta_offset_safe(
            radius=RFLEX_ANCHOR_RADIUS0,
            chord=0,
            angle_resolution=ANGLE_RESOLUTION,
        ),
        angles=(-connector1_angle, connector1_angle),
        geometry_layer=LAYERS.DEVICE_P3,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,  # Solid
    )

    # Outer connection
    _ = c << gl.basic.ring(
        radius_inner=RFLEX_ANCHOR_RADIUS1
        + R_CONNECTOR_CLEARANCE
        - gl.utils.sagitta_offset_safe(
            radius=RFLEX_ANCHOR_RADIUS1 + R_CONNECTOR_CLEARANCE,
            chord=0,
            angle_resolution=ANGLE_RESOLUTION,
        ),
        radius_outer=RDRIVE_INNER_RADIUS
        + gl.utils.sagitta_offset_safe(
            radius=RDRIVE_INNER_RADIUS,
            chord=0,
            angle_resolution=ANGLE_RESOLUTION,
        ),
        angles=(-RDRIVE_ROTOR_SPAN / 2, RSENSOR_START_ANGLE),
        geometry_layer=LAYERS.DEVICE_P3,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=RELEASE_SPEC,
    )

    # Electrical Isolation
    _ = c << gl.basic.ring(
        radius_inner=RFLEX_ANCHOR_RADIUS1,
        radius_outer=RFLEX_ANCHOR_RADIUS1 + R_CONNECTOR_ISOLATION,
        angles=(0, RSENSOR_START_ANGLE),
        geometry_layer=LAYERS.DEVICE_REMOVE,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )

    _ = c << gl.basic.ring(
        radius_inner=RFLEX_ANCHOR_RADIUS0 - R_CONNECTOR_ISOLATION,
        radius_outer=RFLEX_ANCHOR_RADIUS0,
        angles=(-RFLEX_BEAM_ANGLES[0] * 0.75, 0),
        geometry_layer=LAYERS.DEVICE_REMOVE,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )

    hor_iso = c << gf.components.rectangle(
        size=(
            RFLEX_ANCHOR_RADIUS1 - RFLEX_ANCHOR_RADIUS0 + 2 * R_CONNECTOR_ISOLATION,
            R_CONNECTOR_ISOLATION,
        ),
        layer=LAYERS.DEVICE_REMOVE,
        centered=True,
    )
    hor_iso.movex(0.5 * (RFLEX_ANCHOR_RADIUS0 + RFLEX_ANCHOR_RADIUS1))

    # Intermediate stage handle ring
    _ = c << gl.basic.ring(
        radius_inner=RDRIVE_MID_RADIUS + 0.5 * CAVITY_WIDTH,
        radius_outer=ZDRIVE_OUTER_RADIUS,
        angles=(-90, 90),
        geometry_layer=LAYERS.HANDLE_P1,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )

    handle_connector_inner_radius = RFLEX_ANCHOR_RADIUS1 - gl.utils.sagitta_offset_safe(
        radius=RFLEX_ANCHOR_RADIUS1,
        chord=0,
        angle_resolution=ANGLE_RESOLUTION,
    )
    handle_connector_outer_radius = (
        RDRIVE_MID_RADIUS
        + 0.5 * CAVITY_WIDTH
        + gl.utils.sagitta_offset_safe(
            radius=RDRIVE_MID_RADIUS + 0.5 * CAVITY_WIDTH,
            chord=0,
            angle_resolution=ANGLE_RESOLUTION,
        )
    )

    # Handle anchor base (thin part)
    handle_anchor_base = gl.basic.ring(
        radius_inner=handle_connector_inner_radius,
        radius_outer=handle_connector_outer_radius,
        angles=(-90, -90 + 0.5 * RDRIVE_ANCHOR_BASE_SPAN),
        geometry_layer=LAYERS.HANDLE_P1,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )

    (c << handle_anchor_base)
    (c << handle_anchor_base).mirror_y()

    # Handle stopper for R stage
    rstopper: gf.Component = gl.basic.ring(
        radius_inner=handle_connector_outer_radius - RSTOPPER_LENGTH - CAVITY_WIDTH / 2,
        radius_outer=handle_connector_outer_radius,
        angles=(-RSTOPPER_SPAN / 2, RSTOPPER_SPAN / 2),
        geometry_layer=LAYERS.HANDLE_P1,
        angle_resolution=1,
        release_spec=None,
    )
    for angle in [-45, 45]:
        (c << rstopper).rotate(angle)

    # c.flatten()
    return c


@static_cell
def r_sensor_half() -> gf.Component:
    c = gf.Component()
    c << gl.actuator.angular_comb(
        radius_inner=RFLEX_ANCHOR_RADIUS1 + R_CONNECTOR_CLEARANCE,
        radius_outer=RDRIVE_INNER_RADIUS
        + gl.utils.sagitta_offset_safe(
            radius=RDRIVE_INNER_RADIUS,
            chord=0,
            angle_resolution=ANGLE_RESOLUTION,
        ),
        angles=(RSENSOR_START_ANGLE, RSENSOR_END_ANGLE),
        comb_gap=RSENSOR_COMB_GAP,
        comb_count=RSENSOR_COMB_COUNT,
        comb_overlap_angle=RSENSOR_COMB_OVERLAP,
        geometry_layer=LAYERS.DEVICE_P3,
        angle_resolution=ANGLE_RESOLUTION,
    )
    return c


@static_cell
def crossing(radius: float, separation: float, layer1, layer2, layer_handle):
    c = gf.Component()
    (c << via(layer1)).movex(-separation / 2)
    (c << via(layer2)).movex(separation / 2)

    # Rounded rectangle on handle
    c << gf.components.rectangle(
        size=(separation, 2 * radius),
        centered=True,
        layer=layer_handle,
    )
    semi = gf.components.ring(
        radius=radius / 2,
        width=radius,
        layer=layer_handle,
        angle=180,
    )
    (c << semi).rotate(-90).movex(separation / 2)
    (c << semi).rotate(90).movex(-separation / 2)

    return c


@static_cell
def electrical_interconnect() -> gf.Component:

    via1_radius = (
        RDRIVE_MID_RADIUS + CAVITY_WIDTH / 2 + VIA_HANDLE_CLEARANCE + VIA_RADIUS
    )
    via2_radius = via1_radius + VIA_VIA_CLEARANCE
    x_center = (via1_radius + via2_radius) / 2
    handle_height = 2 * (VIA_HANDLE_CLEARANCE + VIA_RADIUS)
    handle_rounded_radius = VIA_HANDLE_CLEARANCE + VIA_RADIUS

    cross = crossing(
        radius=handle_rounded_radius,
        separation=VIA_VIA_CLEARANCE,
        layer1=LAYERS.DEVICE_P5,
        layer2=LAYERS.DEVICE_P5,
        layer_handle=LAYERS.HANDLE_P0,
    )
    # (
    #     c
    #     << gf.components.rectangle(
    #         size=(10, 100), centered=True, layer=LAYERS.DEVICE_P0
    #     )
    # ).move((x_center, 0))

    c = gf.Component()

    for angle in [0, -180]:
        (c << cross).movex(x_center).rotate(angle)

    cross_mid = crossing(
        radius=handle_rounded_radius,
        separation=VIA_VIA_CLEARANCE,
        layer1=LAYERS.DEVICE_P4,
        layer2=LAYERS.DEVICE_P4,
        layer_handle=LAYERS.HANDLE_P0,
    )
    (c << cross_mid).rotate(90).movey(-x_center)

    c << gl.basic.ring(
        radius_inner=via2_radius - 0.5 * ELEC_ROUTING_WIDTH,
        radius_outer=via2_radius + 0.5 * ELEC_ROUTING_WIDTH,
        angles=(-90, -85),
        geometry_layer=LAYERS.DEVICE_P4,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )

    c << gl.basic.ring(
        radius_inner=via1_radius - 0.5 * ELEC_ROUTING_WIDTH,
        radius_outer=via1_radius + 0.5 * ELEC_ROUTING_WIDTH,
        angles=(-95, -90),
        geometry_layer=LAYERS.DEVICE_P4,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )

    c << gl.basic.ring(
        radius_inner=RDRIVE_OUTER_RADIUS + 2 * DEVICE_ISOLATION + ELEC_ROUTING_WIDTH,
        radius_outer=RDRIVE_OUTER_RADIUS
        + 2 * DEVICE_ISOLATION
        + 2 * ELEC_ROUTING_WIDTH,
        angles=(-181, 1),
        geometry_layer=LAYERS.DEVICE_P5,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )

    wire1 = gl.basic.ring(
        radius_inner=RDRIVE_OUTER_RADIUS + DEVICE_ISOLATION,
        radius_outer=RDRIVE_OUTER_RADIUS + DEVICE_ISOLATION + ELEC_ROUTING_WIDTH,
        angles=(-80, RDRIVE_PHASE_SPAN + 1),
        geometry_layer=LAYERS.DEVICE_P6,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )
    (c << wire1)
    (c << wire1).mirror_x()

    c << gl.basic.ring(
        radius_inner=RDRIVE_MID_RADIUS + RDRIVE_TEETH_HEIGHT + DEVICE_ISOLATION,
        radius_outer=RDRIVE_OUTER_RADIUS + DEVICE_ISOLATION + ELEC_ROUTING_WIDTH,
        angles=(-93, -87),
        geometry_layer=LAYERS.DEVICE_P6,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )

    # Overrides on DEVICE layer to make connections complete
    c << gl.basic.ring(
        radius_inner=RDRIVE_MID_RADIUS + RDRIVE_TEETH_HEIGHT + DEVICE_ISOLATION,
        radius_outer=RDRIVE_OUTER_RADIUS,
        angles=(-87, -RDRIVE_STATOR_SPAN_MIN / 2),
        geometry_layer=LAYERS.DEVICE,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )
    c << gl.basic.ring(
        radius_inner=RDRIVE_MID_RADIUS + RDRIVE_TEETH_HEIGHT + DEVICE_ISOLATION,
        radius_outer=RDRIVE_OUTER_RADIUS,
        angles=(-180 + RDRIVE_STATOR_SPAN_MIN / 2, -95),
        geometry_layer=LAYERS.DEVICE,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )
    c << gl.basic.ring(
        radius_inner=RDRIVE_OUTER_RADIUS + DEVICE_ISOLATION,
        radius_outer=RDRIVE_OUTER_RADIUS + DEVICE_ISOLATION + ELEC_ROUTING_WIDTH,
        angles=(-85, -80),
        geometry_layer=LAYERS.DEVICE,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )
    c << gl.basic.ring(
        radius_inner=RDRIVE_OUTER_RADIUS + DEVICE_ISOLATION,
        radius_outer=RDRIVE_OUTER_RADIUS + DEVICE_ISOLATION + ELEC_ROUTING_WIDTH,
        angles=(-100, -93),
        geometry_layer=LAYERS.DEVICE,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )

    conn = gl.basic.ring(
        radius_inner=RDRIVE_OUTER_RADIUS
        - gl.utils.sagitta_offset_safe(
            radius=RDRIVE_OUTER_RADIUS,
            chord=0,
            angle_resolution=ANGLE_RESOLUTION,
        ),
        radius_outer=RDRIVE_OUTER_RADIUS
        + DEVICE_ISOLATION
        + gl.utils.sagitta_offset_safe(
            radius=RDRIVE_OUTER_RADIUS + DEVICE_ISOLATION,
            chord=0,
            angle_resolution=ANGLE_RESOLUTION,
        ),
        angles=(RDRIVE_PHASE_SPAN - 1, RDRIVE_PHASE_SPAN + 1),
        geometry_layer=LAYERS.DEVICE,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )
    (c << conn)
    (c << conn).mirror_x()

    return c


@static_cell
def device(text: str) -> gf.Component:
    c = gf.Component()

    # Emit chip border
    chip_border_ref = c << chip_border()

    # Emit central carriage and tip
    center_carriage_ref = c << center_carriage()

    # Generate rotator
    r_flexure = r_flexure_full()
    (c << r_flexure)

    # r_flexure_half_lower_ref = c << r_flexure_half()
    # r_flexure_half_lower_ref.rotate(angle=90, center=(0, 0))
    # r_flexure_half_lower_ref.mirror_y(0)

    rdr_half: gf.Component = r_drive_half()
    (c << rdr_half)
    (c << rdr_half).mirror_x(0)

    rconn_half: gf.Component = r_connectors_half()
    (c << rconn_half)
    (c << rconn_half).mirror_x(0)

    rsen_half: gf.Component = r_sensor_half()
    (c << rsen_half)
    (c << rsen_half).mirror_x(0)

    c << electrical_interconnect()

    # # Emit label
    # c << build_label()

    # # Emit zstage
    # c << build_zstage()

    # # Emit rotator
    # c << build_rotator()
    return c
