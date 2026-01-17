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
DEVICE_ISOLATION = 7
ELEC_ROUTING_WIDTH = 70

RELEASE_SPEC = gl.datatypes.ReleaseSpec(
    hole_radius=3.3,
    distance=6,
    angle_resolution=18,
    layer=LAYERS.DEVICE_REMOVE,
)

RELEASE_SPEC_CHIP_BORDER = gl.datatypes.ReleaseSpec(
    hole_radius=3.3,
    distance=8,
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
RFLEX_BEAM_WIDTH = 2.6
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
RDRIVE_TEETH_CLEARANCE = 2.0
RDRIVE_TEETH_PHASE = [-120, 0, 120]
RDRIVE_PHASE_SPAN = 40
RDRIVE_TEETH_COUNT = int(np.floor(RDRIVE_PHASE_SPAN / RDRIVE_TEETH_PITCH))
RDRIVE_ROTOR_SPAN = 150
RDRIVE_STATOR_SPAN_MIN = RDRIVE_PHASE_SPAN * len(RDRIVE_TEETH_PHASE)
RDRIVE_ANCHOR_BASE_SPAN = 20

ZSTAGE_OUTER_RADIUS = 1280
ZSTAGE_EXTENSION = (760, 150)

HANDLE_DEVICE_SUPPORT_ANGLE = 60
HANDLE_SPLIT_ANGLE = 25

RSENSOR_START_ANGLE = 40
RSENSOR_END_ANGLE = 88
RSENSOR_COMB_GAP = 5
RSENSOR_COMB_WIDTH = 6
RSENSOR_COMB_COUNT = int(
    np.floor(
        (RDRIVE_INNER_RADIUS - RFLEX_ANCHOR_RADIUS1 - RSENSOR_COMB_WIDTH)
        / (RSENSOR_COMB_GAP + RSENSOR_COMB_WIDTH)
    )
)
RSENSOR_COMB_OVERLAP = 19
RSENSOR_LEAD_WIDTH = 18
RSENSOR_LEAD_LENGTH = ZSTAGE_OUTER_RADIUS - RFLEX_ANCHOR_RADIUS1
RSENSOR_LEAD_GAP = 30

R_CONNECTOR_CLEARANCE = 10  # Mechanical clearance

RINTERCONN_VIAS_ANGLE = 0

RSTOPPER_ANGLE = 45
RSTOPPER_SPAN = 3
RSTOPPER_LENGTH = 25

RANCHOR_ANGLE = RFLEX_BEAM_ANGLES[0] + 0.5 * RFLEX_BEAM_WIDTH / RFLEX_ANCHOR_RADIUS0 / (
    np.pi / 180
)


Z_RELEASE_LOCK_SPAN = (40, 50)

ZCANT_CLEARANCE = 8
ZCANT_ROUTING_CLEARANCE = 15
ZCANT_WIDTH = 400
ZCANT_LENGTH = 600
ZCANT_POSITION = ZSTAGE_OUTER_RADIUS + ZSTAGE_EXTENSION[1] + CAVITY_WIDTH - 120
ZCANT_BOTTOM_CURVATURE = 600

ZCANT_BEAM_MAIN_WIDTH = 8
ZCANT_BEAM_MAIN_LENGTH = 80


ZCANT_BEAM_DRIVE_WIDTH = 4
ZCANT_BEAM_DRIVE_LENGTH = 100
ZCANT_BEAM_DRIVE_FRACTION = 0.8  # Controls lever ratio


ZCANT_ANCHOR_SIZE = (100, 100)

ZCLAMP_WIDTH = 100
ZCLAMP_LENGTH1 = 280
ZCLAMP_LENGTH2 = 840

ZCLAMP_BEAM_WIDTH = 4
ZCLAMP_BEAM_LENGTH = 50
ZCLAMP_ANCHOR_SIZE = (100, 100)
ZCLAMP_BEAM_POS = [0, 1]

ZCLAMP_POS = (
    ZCANT_POSITION
    - ZCANT_ANCHOR_SIZE[0] / 2
    - ZCLAMP_ANCHOR_SIZE[0] / 2
    - ZCANT_CLEARANCE,
    -(
        ZCANT_WIDTH / 2
        + ZCANT_BEAM_MAIN_LENGTH
        + ZCANT_ANCHOR_SIZE[1]
        + ZCLAMP_BEAM_LENGTH
        + ZCLAMP_WIDTH
    ),
)

ZCLAMP_PFLEX_BEAM_WIDTH = 5
ZCLAMP_PFLEX_BEAM_LENGTH = 600
ZCLAMP_PFLEX_BAR_WIDTH = 50
ZCLAMP_PFLEX_BAR_LENGTH = 490
ZCLAMP_PFLEX_STROKE = 25
ZCLAMP_PFLEX_BEAM_POS = [0, 0.08, 0.92, 1]
ZCLAMP_PFLEX_ANCHOR_SIZE = (100, 100)
ZCLAMP_PFLEX_POS = (
    ZCLAMP_POS[0] + ZCLAMP_PFLEX_BEAM_LENGTH + 150,
    ZCLAMP_POS[1]
    - ZCLAMP_PFLEX_BAR_LENGTH / 2
    - CAVITY_WIDTH
    - ZCLAMP_PFLEX_ANCHOR_SIZE[1],
)
ZCLAMP_PFLEX_BEAM_SPEC = gl.datatypes.BeamSpec(
    release_thick=True,
    thick_length=(0, 0.7),
    thick_width=(18, 0),
    thick_offset=(0, 0),
)
ZCLAMP_PECK_OVERLAP = 25
ZCLAMP_PECK_WIDTH = 50
ZCLAMP_CARRIAGE_WIDTH = 33
ZCLAMP_CARRIAGE_SPACING = 30

ZCLAMP_COMB_GAP = 3.5
ZCLAMP_COMB_WIDTH = 4
ZCLAMP_COMB_COUNT = 110
ZCLAMP_COMB_HEIGHT = 70
ZCLAMP_COMB_OVERLAP = ZCLAMP_COMB_HEIGHT - 10 - 2 * ZCLAMP_PFLEX_STROKE
ZCLAMP_COMB_ANCHOR_WIDTH = 25

Z_CANT_BEAM_SPEC = None

ZACTUATOR_SIZE = (900, 1700)
ZACTUATOR_POS = (1280, 480)
ZACTUATOR_ANCHOR_SIZE = (100, 100)
ZACTUATOR_BEAM_LENGTH = 50
ZACTUATOR_BEAM_WIDTH = 4
ZACTUATOR_CONN_WIDTH = 300

ZCANT_BEAM_STOPPER_INNER_WIDTH = 75
ZCANT_BEAM_STOPPER_INNER_INSET = (75, 0)
ZCANT_BEAM_STOPPER_INNER_LENGTH = (
    ZCANT_BEAM_STOPPER_INNER_INSET[0]
    - ZCLAMP_POS[1]
    - ZCLAMP_WIDTH
    - ZCANT_WIDTH / 2
    - ZCLAMP_BEAM_LENGTH
    - ZCLAMP_ANCHOR_SIZE[1]
)
ZCANT_BEAM_STOPPER_INNER_POS = (ZCLAMP_POS[0] + ZCLAMP_LENGTH1 - ZCANT_POSITION, 0)


ZCANT_BEAM_STOPPER_OUTER_WIDTH = 50
ZCANT_BEAM_STOPPER_OUTER_INSET = (0, 0.4)
ZCANT_BEAM_STOPPER_OUTER_LENGTH = CAVITY_WIDTH + 50
ZCANT_BEAM_STOPPER_OUTER_POS = (ZCANT_BEAM_STOPPER_OUTER_WIDTH / 2, 0.6)

WIRE_BOND_SIZE = 400
WIRE_BOND_OFFSET = 300
WIRE_BOND_POS = [-1300, -150, 500, 1500, 2400]
WIRE_BOND_GROUNDED_INDICES = [3]

LABEL_REGION_SIZE = (500, 600)
LABEL_TEXT_SIZE = 70
LABEL_POSITION = (-2500, 1850)
LABELS = {
    220: "MEGA-2D",
    100: "Cao Lab",
    20: "EECS",
    -60: "Berkeley",
    -140: "",
    -210: "Ver 0.9",
    -290: "ZRLock",
}
VIA_RADIUS = 20
VIA_DEVICE_CLEARANCE = 25
VIA_HANDLE_CLEARANCE = 40
VIA_VIA_CLEARANCE = 2 * (VIA_RADIUS + VIA_DEVICE_CLEARANCE) + 20

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
        release_spec=RELEASE_SPEC_CHIP_BORDER,
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
        geometry_layer=LAYERS.DEVICE_P3_NOISO,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )

    anchor_dev_expand: gf.Component = gl.basic.ring(
        radius_inner=RFLEX_ANCHOR_RADIUS0,
        radius_outer=RFLEX_ANCHOR_RADIUS1 + R_CONNECTOR_CLEARANCE,
        angles=(90 - RANCHOR_ANGLE, 90 + RANCHOR_ANGLE),
        geometry_layer=LAYERS.DEVICE_P3_NOISO,
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
        radius_outer=RFLEX_ANCHOR_RADIUS1 + DEVICE_ISOLATION,
        angles=(0, RSENSOR_START_ANGLE),
        geometry_layer=LAYERS.DEVICE_REMOVE,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )

    _ = c << gl.basic.ring(
        radius_inner=RFLEX_ANCHOR_RADIUS0 - DEVICE_ISOLATION,
        radius_outer=RFLEX_ANCHOR_RADIUS0,
        angles=(-RFLEX_BEAM_ANGLES[0] * 0.75, 0),
        geometry_layer=LAYERS.DEVICE_REMOVE,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )

    hor_iso = c << gf.components.rectangle(
        size=(
            RFLEX_ANCHOR_RADIUS1 - RFLEX_ANCHOR_RADIUS0 + 2 * DEVICE_ISOLATION,
            DEVICE_ISOLATION,
        ),
        layer=LAYERS.DEVICE_REMOVE,
        centered=True,
    )
    hor_iso.movex(0.5 * (RFLEX_ANCHOR_RADIUS0 + RFLEX_ANCHOR_RADIUS1))

    # Intermediate stage handle ring
    _ = c << gl.basic.ring(
        radius_inner=RDRIVE_MID_RADIUS + 0.5 * CAVITY_WIDTH,
        radius_outer=ZSTAGE_OUTER_RADIUS,
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
        geometry_layer=LAYERS.DEVICE_P3_NOISO,
        angle_resolution=ANGLE_RESOLUTION,
    )

    lead = c << gf.components.rectangle(
        size=(RSENSOR_LEAD_WIDTH, RSENSOR_LEAD_LENGTH),
        centered=False,
        layer=LAYERS.DEVICE_P4,
    )
    lead.move((RSENSOR_LEAD_GAP / 2, RFLEX_ANCHOR_RADIUS1 + DEVICE_ISOLATION))
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
        layer1=LAYERS.DEVICE_P3,
        layer2=LAYERS.DEVICE_P5,
        layer_handle=LAYERS.HANDLE_P0,
    )

    c = gf.Component()

    for angle in [RINTERCONN_VIAS_ANGLE, -180 - RINTERCONN_VIAS_ANGLE]:
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
        radius_outer=ZSTAGE_OUTER_RADIUS,
        angles=(-180 - RINTERCONN_VIAS_ANGLE - 1, RINTERCONN_VIAS_ANGLE + 1),
        geometry_layer=LAYERS.DEVICE_P5,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )

    wire1 = gl.basic.ring(
        radius_inner=RDRIVE_OUTER_RADIUS + DEVICE_ISOLATION,
        radius_outer=RDRIVE_OUTER_RADIUS + DEVICE_ISOLATION + ELEC_ROUTING_WIDTH,
        angles=(-80, RDRIVE_PHASE_SPAN / 2 + 3),
        geometry_layer=LAYERS.DEVICE_P6,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )
    (c << wire1)
    (c << wire1).mirror_x()

    c << gl.basic.ring(
        radius_inner=RDRIVE_MID_RADIUS + RDRIVE_TEETH_HEIGHT + DEVICE_ISOLATION,
        radius_outer=RDRIVE_OUTER_RADIUS + DEVICE_ISOLATION + ELEC_ROUTING_WIDTH,
        angles=(-94, -86),
        geometry_layer=LAYERS.DEVICE_P6,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )

    # Overrides on DEVICE layer to make connections complete
    # Connect left C phase with middle crossing
    c << gl.basic.ring(
        radius_inner=RDRIVE_MID_RADIUS + RDRIVE_TEETH_HEIGHT + DEVICE_ISOLATION,
        radius_outer=RDRIVE_OUTER_RADIUS,
        angles=(-87, -RDRIVE_STATOR_SPAN_MIN / 2),
        geometry_layer=LAYERS.DEVICE,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )
    # Connect right A phase with middle crossing
    c << gl.basic.ring(
        radius_inner=RDRIVE_MID_RADIUS + RDRIVE_TEETH_HEIGHT + DEVICE_ISOLATION,
        radius_outer=RDRIVE_OUTER_RADIUS,
        angles=(-180 + RDRIVE_STATOR_SPAN_MIN / 2, -95),
        geometry_layer=LAYERS.DEVICE,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )
    # Connect right C phase routing with middle crossing
    c << gl.basic.ring(
        radius_inner=RDRIVE_OUTER_RADIUS + DEVICE_ISOLATION,
        radius_outer=RDRIVE_OUTER_RADIUS + DEVICE_ISOLATION + ELEC_ROUTING_WIDTH,
        angles=(-85, -80),
        geometry_layer=LAYERS.DEVICE,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )
    # Connect left A phase routing with middle crossing
    c << gl.basic.ring(
        radius_inner=via1_radius + ELEC_ROUTING_WIDTH / 2 + DEVICE_ISOLATION,
        radius_outer=RDRIVE_OUTER_RADIUS + DEVICE_ISOLATION + ELEC_ROUTING_WIDTH,
        angles=(-100, -93),
        geometry_layer=LAYERS.DEVICE,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )

    # Connect left A and right C phases routing with their drives
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
        angles=(RDRIVE_PHASE_SPAN / 2 + 1, RDRIVE_PHASE_SPAN / 2 + 3),
        geometry_layer=LAYERS.DEVICE_P3_NOISO,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )
    (c << conn)
    (c << conn).mirror_x()

    # Connect A and C phase to zcant
    p1 = (
        (RDRIVE_OUTER_RADIUS + DEVICE_ISOLATION + 0.5 * ELEC_ROUTING_WIDTH),
        ELEC_ROUTING_WIDTH,
    )
    p2 = (
        ZCANT_POSITION - ELEC_ROUTING_WIDTH * 0.5 - ZCANT_ROUTING_CLEARANCE,
        -ZCANT_WIDTH / 2 - ZCANT_BEAM_MAIN_LENGTH,
    )
    pmid = (p2[0], p1[1])
    path = gf.path.smooth(
        points=np.array([p1, pmid, p2]),
        radius=ELEC_ROUTING_WIDTH / 2,
    )
    (c << path.extrude(layer=LAYERS.DEVICE_P6, width=ELEC_ROUTING_WIDTH))
    (c << path.extrude(layer=LAYERS.DEVICE_P6, width=ELEC_ROUTING_WIDTH)).mirror_x()

    # Connect B phase to zcant
    p1 = (
        ZCANT_WIDTH / 2 + ZCANT_BEAM_MAIN_LENGTH + ZCANT_ANCHOR_SIZE[1] / 2,
        -ZCANT_POSITION,
    )
    p2 = (p1[0], -(ZSTAGE_OUTER_RADIUS - ELEC_ROUTING_WIDTH))
    path = gf.path.smooth(
        points=np.array([p1, p2]),
        radius=ELEC_ROUTING_WIDTH / 2,
    )
    (c << path.extrude(layer=LAYERS.DEVICE_P5, width=ELEC_ROUTING_WIDTH))

    # Connect zcant to ground
    (c << via(LAYERS.DEVICE_P3)).move((-p1[0], p1[1]))
    (c << via(LAYERS.DEVICE_P3)).move((-p1[0], -p1[1]))

    # Connect ground to RDrive
    (c << via(LAYERS.DEVICE_P3)).move(
        (0, -0.5 * (RFLEX_ANCHOR_RADIUS0 + RFLEX_ANCHOR_RADIUS1))
    )

    # Connect tip bias to R Flexure top anchor
    p1 = (
        ZCANT_WIDTH / 2 + ZCANT_BEAM_MAIN_LENGTH + ZCANT_ANCHOR_SIZE[1] / 2,
        ZCANT_POSITION - ELEC_ROUTING_WIDTH * 0.5 - ZCANT_ROUTING_CLEARANCE,
    )
    p2 = (0, 0.5 * (RFLEX_ANCHOR_RADIUS0 + RFLEX_ANCHOR_RADIUS1))

    pmid = (p2[0], p1[1])
    path = gf.path.smooth(
        points=np.array([p1, pmid, p2]),
        radius=ELEC_ROUTING_WIDTH / 2,
    )
    (c << path.extrude(layer=LAYERS.DEVICE_P5, width=ELEC_ROUTING_WIDTH))

    # Connect Right Rsensor to Zcant
    path = gf.Path()
    radius = ZSTAGE_OUTER_RADIUS - ELEC_ROUTING_WIDTH / 2 - ZCANT_ROUTING_CLEARANCE
    startangle = (
        np.asin((RSENSOR_LEAD_GAP + RSENSOR_LEAD_WIDTH) / 2 / radius) / np.pi * 180
    )
    angle = (
        np.acos((ZSTAGE_EXTENSION[0] / 2 - ZCANT_ANCHOR_SIZE[1] / 2) / radius)
        / np.pi
        * 180
    )

    path += gf.path.arc(radius=radius, angle=startangle - angle)
    path += gf.path.arc(radius=0.001, angle=angle)
    path += gf.path.straight(ZCANT_POSITION - radius * np.sin(angle / 180 * np.pi))

    path.rotate(-startangle)
    path.move(((RSENSOR_LEAD_GAP + RSENSOR_LEAD_WIDTH) / 2, radius))
    (c << path.extrude(layer=LAYERS.DEVICE_P4, width=ELEC_ROUTING_WIDTH))

    # Connect Left Rsensor to Zcant
    path = gf.Path()
    radius = ZSTAGE_OUTER_RADIUS - ELEC_ROUTING_WIDTH / 2 - ZCANT_ROUTING_CLEARANCE
    startangle = (
        np.asin((RSENSOR_LEAD_GAP + RSENSOR_LEAD_WIDTH) / 2 / radius) / np.pi * 180
    )
    y4 = (
        ZCANT_WIDTH / 2
        + ZCANT_BEAM_MAIN_LENGTH
        + ZCANT_ANCHOR_SIZE[1] / 2
        - ELEC_ROUTING_WIDTH * 2
    )
    angle = np.acos((y4) / radius) / np.pi * 180

    path += gf.path.arc(radius=radius, angle=startangle - angle)
    path += gf.path.arc(radius=0.001, angle=angle)
    path += gf.path.straight(
        ZCANT_POSITION
        - ELEC_ROUTING_WIDTH * 0.5
        - ZCANT_ROUTING_CLEARANCE
        - radius * np.sin(angle / 180 * np.pi)
    )
    path += gf.path.arc(radius=0.001, angle=90)
    path += gf.path.straight(
        ZCANT_WIDTH / 2 + ZCANT_BEAM_MAIN_LENGTH + ZCANT_ANCHOR_SIZE[1] / 2 - y4
    )

    path.rotate(-startangle)
    path.move(((RSENSOR_LEAD_GAP + RSENSOR_LEAD_WIDTH) / 2, radius))
    (c << path.extrude(layer=LAYERS.DEVICE_P4, width=ELEC_ROUTING_WIDTH)).mirror_x()

    return c


@static_cell
def z_cant() -> gf.Component:
    c = gf.Component()

    # ZStage extension
    ext = c << gf.components.rectangle(
        size=(ZSTAGE_EXTENSION[0], 2 * ZSTAGE_EXTENSION[1]),
        layer=LAYERS.HANDLE_P1,
        centered=True,
    )
    ext.movey(ZSTAGE_OUTER_RADIUS)

    # Z cantilever

    beam_main_0 = gl.flexure.ZCantileverBeam(
        length=ZCANT_BEAM_MAIN_LENGTH,
        width=ZCANT_BEAM_MAIN_WIDTH,
        position=(-0.5 * ZCANT_BEAM_MAIN_WIDTH, 1.0),
        inset_x=(0, 0),
        inset_y=(0, 0),
        isolation_x=(0, 0),
        isolation_y=(0, 0),
        spec=Z_CANT_BEAM_SPEC,
    )

    beam_main_1 = gl.flexure.ZCantileverBeam(
        length=ZCANT_BEAM_MAIN_LENGTH,
        width=ZCANT_BEAM_MAIN_WIDTH,
        position=(0.5 * ZCANT_BEAM_MAIN_WIDTH, 0.0),
        inset_x=(0, 0),
        inset_y=(0, 0),
        isolation_x=(0, 0),
        isolation_y=(0, 0),
        spec=Z_CANT_BEAM_SPEC,
    )

    beam_drive = gl.flexure.ZCantileverBeam(
        length=ZCANT_BEAM_DRIVE_LENGTH,
        width=ZCANT_BEAM_DRIVE_WIDTH,
        position=(0, ZCANT_BEAM_DRIVE_FRACTION),
        inset_x=(0, 0),
        inset_y=(0, 0),
        isolation_x=(0, 1 - ZCANT_BEAM_DRIVE_FRACTION),
        isolation_y=(0, 0.25),
        spec=Z_CANT_BEAM_SPEC,
    )

    beam_stopper_inner = gl.flexure.ZCantileverBeam(
        length=ZCANT_BEAM_STOPPER_INNER_LENGTH,
        width=ZCANT_BEAM_STOPPER_INNER_WIDTH,
        position=ZCANT_BEAM_STOPPER_INNER_POS,
        inset_x=(ZCANT_BEAM_STOPPER_INNER_WIDTH, 0),
        inset_y=ZCANT_BEAM_STOPPER_INNER_INSET,
        isolation_x=(ZCANT_BEAM_STOPPER_INNER_WIDTH, 0),
        isolation_y=ZCANT_BEAM_STOPPER_INNER_INSET,
        spec=gl.datatypes.BeamSpec(release_thin=True),
    )

    beam_stopper_outer = gl.flexure.ZCantileverBeam(
        length=ZCANT_BEAM_STOPPER_OUTER_LENGTH,
        width=ZCANT_BEAM_STOPPER_OUTER_WIDTH,
        position=ZCANT_BEAM_STOPPER_OUTER_POS,
        inset_x=(0, 0),
        inset_y=(0, 0),
        isolation_x=(ZCANT_BEAM_STOPPER_OUTER_WIDTH, 0),
        isolation_y=ZCANT_BEAM_STOPPER_OUTER_INSET,
        spec=gl.datatypes.BeamSpec(release_thin=True),
    )

    zcant_half_drive = gl.flexure.z_cantilever_half(
        length=ZCANT_LENGTH,
        width=ZCANT_WIDTH,
        beams=[beam_main_0, beam_main_1, beam_drive],
        clearance=ZCANT_CLEARANCE,
        middle_split=True,
        geometry_layer=LAYERS.DEVICE_P3,
        handle_layer=LAYERS.HANDLE_P0,
        release_spec=Z_CANT_BEAM_SPEC,
    )

    zcant_half_nodrive = gl.flexure.z_cantilever_half(
        length=ZCANT_LENGTH,
        width=ZCANT_WIDTH,
        beams=[beam_main_0, beam_main_1, beam_stopper_inner, beam_stopper_outer],
        clearance=ZCANT_CLEARANCE,
        middle_split=True,
        geometry_layer=LAYERS.DEVICE_P3,
        handle_layer=LAYERS.HANDLE_P0,
        release_spec=RELEASE_SPEC,
    )

    anchor1 = gf.Component()
    anchor1 << gf.components.rectangle(
        size=ZCANT_ANCHOR_SIZE, layer=LAYERS.DEVICE_P3_NOISO, centered=True
    )
    anchor1.move(
        (
            ZCANT_POSITION,
            ZCANT_WIDTH / 2 + ZCANT_BEAM_MAIN_LENGTH + ZCANT_ANCHOR_SIZE[1] / 2,
        )
    )

    (c << zcant_half_drive).movex(ZCANT_POSITION)
    (c << zcant_half_nodrive).mirror_y().movex(ZCANT_POSITION)
    (c << anchor1)
    (c << anchor1).mirror_y()
    (c << anchor1).movex(ZCANT_LENGTH)
    (c << anchor1).movex(ZCANT_LENGTH).mirror_y()

    # Generate bottom curvature on zcant
    sub = gf.Component()
    circ = sub << gf.components.circle(
        radius=ZCANT_BOTTOM_CURVATURE,
        angle_resolution=ANGLE_RESOLUTION,
        layer=LAYERS.HANDLE_P0,
    )
    circ.movex(ZCANT_POSITION - np.sqrt(ZCANT_BOTTOM_CURVATURE**2 - ZCANT_WIDTH**2 / 4))
    handle_curved = gf.boolean(
        A=c,
        B=sub,
        operation="-",
        layer=LAYERS.HANDLE_P0,
        layer1=LAYERS.HANDLE_P0,
        layer2=LAYERS.HANDLE_P0,
    )

    c.remove_layers([LAYERS.HANDLE_P0])
    c << handle_curved

    # Connect zcant to bonding pads

    p1 = (
        ZCANT_POSITION + ZCANT_LENGTH,
        ZCANT_WIDTH / 2 + ZCANT_BEAM_MAIN_LENGTH + ZCANT_ANCHOR_SIZE[1] / 2,
    )
    p2 = (CHIP_SIZE / 2 - WIRE_BOND_OFFSET - WIRE_BOND_SIZE / 2, WIRE_BOND_POS[2])
    pmid = (p2[0], p1[1])
    path = gf.path.smooth(
        points=np.array([p1, pmid, p2]),
        radius=ELEC_ROUTING_WIDTH / 2,
    )
    (c << path.extrude(layer=LAYERS.DEVICE_P3_NOISO, width=ELEC_ROUTING_WIDTH))

    p1 = (
        ZCANT_POSITION + ZCANT_LENGTH,
        -(ZCANT_WIDTH / 2 + ZCANT_BEAM_MAIN_LENGTH + ZCANT_ANCHOR_SIZE[1] / 2),
    )
    p2 = (CHIP_SIZE / 2 - WIRE_BOND_OFFSET - WIRE_BOND_SIZE / 2, WIRE_BOND_POS[1])
    pmid = (p2[0], p1[1])
    path = gf.path.smooth(
        points=np.array([p1, pmid, p2]),
        radius=ELEC_ROUTING_WIDTH / 2,
    )
    (c << path.extrude(layer=LAYERS.DEVICE_P3_NOISO, width=ELEC_ROUTING_WIDTH))
    return c


@static_cell
def z_actuator() -> gf.Component:
    c = gf.Component()

    z_act = c << gl.basic.rectangle(
        size=ZACTUATOR_SIZE,
        geometry_layer=LAYERS.DEVICE_P3,
        centered=False,
        release_spec=RELEASE_SPEC,
    )

    z_act.move(ZACTUATOR_POS)

    z_act_conn = c << gl.basic.rectangle(
        size=(
            ZACTUATOR_CONN_WIDTH,
            ZACTUATOR_POS[1] - ZCANT_WIDTH / 2 - ZCANT_BEAM_DRIVE_LENGTH,
        ),
        geometry_layer=LAYERS.DEVICE_P3,
        centered=False,
        release_spec=RELEASE_SPEC,
    )

    z_act_conn.move(
        (
            ZACTUATOR_POS[0] + (ZACTUATOR_SIZE[0] - ZACTUATOR_CONN_WIDTH) / 2,
            ZCANT_WIDTH / 2 + ZCANT_BEAM_DRIVE_LENGTH,
        )
    )

    anchor3 = gf.Component()
    beam = anchor3 << gl.flexure.beam(
        length=ZACTUATOR_BEAM_LENGTH,
        width=ZACTUATOR_BEAM_WIDTH,
        geometry_layer=LAYERS.DEVICE_P3,
        beam_spec=None,
        release_spec=None,
    )
    square = anchor3 << gf.components.rectangle(
        size=ZACTUATOR_ANCHOR_SIZE, layer=LAYERS.DEVICE_P3, centered=True
    )
    beam.move(
        (
            ZACTUATOR_POS[0] - ZACTUATOR_BEAM_LENGTH / 2,
            ZACTUATOR_POS[1] + ZACTUATOR_SIZE[1] - ZACTUATOR_BEAM_WIDTH / 2,
        )
    )
    square.move(
        (
            ZACTUATOR_POS[0] - ZACTUATOR_BEAM_LENGTH - ZACTUATOR_ANCHOR_SIZE[0] / 2,
            ZACTUATOR_POS[1] + ZACTUATOR_SIZE[1] - ZACTUATOR_BEAM_WIDTH / 2,
        )
    )

    (c << anchor3)
    (c << anchor3).mirror_x(ZACTUATOR_SIZE[0] / 2 + ZACTUATOR_POS[0])

    return c


@static_cell
def z_clamp() -> gf.Component:
    c = gf.Component()

    # Z clamp lever

    beam0 = gl.flexure.ZCantileverBeam(
        length=ZCLAMP_BEAM_LENGTH,
        width=ZCLAMP_BEAM_WIDTH,
        position=(0.5 * ZCLAMP_BEAM_WIDTH, ZCLAMP_BEAM_POS[0]),
        inset_x=(0, 0),
        inset_y=(0, 0),
        isolation_x=(0, 0),
        isolation_y=(0, 0),
        spec=Z_CANT_BEAM_SPEC,
    )

    beam1 = gl.flexure.ZCantileverBeam(
        length=ZCLAMP_BEAM_LENGTH,
        width=ZCLAMP_BEAM_WIDTH,
        position=(-0.5 * ZCLAMP_BEAM_WIDTH, ZCLAMP_BEAM_POS[1]),
        inset_x=(0, 0),
        inset_y=(0, 0),
        isolation_x=(0, 0),
        isolation_y=(0, 0),
        spec=Z_CANT_BEAM_SPEC,
    )

    beam2 = gl.flexure.ZCantileverBeam(
        length=ZCLAMP_BEAM_LENGTH,
        width=ZCLAMP_BEAM_WIDTH,
        position=(-0.5 * ZCLAMP_BEAM_WIDTH, ZCLAMP_BEAM_POS[1]),
        inset_x=(0, 0),
        inset_y=(0, 0),
        isolation_x=(0, 0),
        isolation_y=(0, 0),
        spec=Z_CANT_BEAM_SPEC,
        flip_side=True,
    )

    zclamp_lever = gl.flexure.z_cantilever_asymm(
        length=ZCLAMP_LENGTH1,
        width=ZCLAMP_WIDTH,
        beams=[beam0, beam1],
        clearance=ZCANT_CLEARANCE,
        geometry_layer=LAYERS.DEVICE_P3,
        handle_layer=LAYERS.HANDLE_P0,
        release_spec=Z_CANT_BEAM_SPEC,
    )

    zclamp_lever_ext = gf.components.rectangle(
        size=(ZCLAMP_LENGTH2, ZCLAMP_WIDTH), layer=LAYERS.HANDLE_P0, centered=False
    )

    (c << zclamp_lever).move(ZCLAMP_POS)
    (c << zclamp_lever_ext).move((ZCLAMP_POS[0] + ZCLAMP_LENGTH1, ZCLAMP_POS[1]))

    anchor2 = gf.Component()
    anchor2 << gf.components.rectangle(
        size=ZCLAMP_ANCHOR_SIZE, layer=LAYERS.DEVICE_P3, centered=True
    )
    anchor2.move(
        (
            ZCLAMP_POS[0],
            ZCLAMP_POS[1]
            + ZCLAMP_WIDTH
            + ZCLAMP_BEAM_LENGTH
            + ZCLAMP_ANCHOR_SIZE[1] / 2,
        )
    )

    (c << anchor2).movex(ZCLAMP_LENGTH1 * ZCLAMP_BEAM_POS[0])
    (c << anchor2).movex(ZCLAMP_LENGTH1 * ZCLAMP_BEAM_POS[1])
    (c << via(LAYERS.DEVICE_P3)).move(
        (
            ZCLAMP_POS[0] + ZCLAMP_LENGTH1 * ZCLAMP_BEAM_POS[1],
            ZCLAMP_POS[1]
            + ZCLAMP_WIDTH
            + ZCLAMP_BEAM_LENGTH
            + ZCLAMP_ANCHOR_SIZE[1] / 2,
        )
    )
    (c << via(LAYERS.DEVICE_P3)).move(
        (
            ZCLAMP_POS[0] + ZCLAMP_LENGTH1 * ZCLAMP_BEAM_POS[1] / 2,
            ZCLAMP_POS[1] + ZCLAMP_WIDTH / 2,
        )
    )
    # (c << anchor2).movex(ZCLAMP_LENGTH1 * ZCLAMP_BEAM_POS[1]).movey(
    #     -ZCLAMP_ANCHOR_SIZE[1] - 2 * ZCLAMP_BEAM_LENGTH - ZCLAMP_WIDTH
    # )

    # Generate comb drive for clamp

    flex = c << gl.flexure.parallel_flexure(
        length_beam=ZCLAMP_PFLEX_BEAM_LENGTH,
        width_beam=ZCLAMP_PFLEX_BEAM_WIDTH,
        length_bar=ZCLAMP_PFLEX_BAR_LENGTH,
        width_bar=ZCLAMP_PFLEX_BAR_WIDTH,
        beam_pos=ZCLAMP_PFLEX_BEAM_POS,
        geometry_layer=LAYERS.DEVICE_P3,
        beam_spec=ZCLAMP_PFLEX_BEAM_SPEC,
        release_spec=RELEASE_SPEC,
    )

    flex.rotate(90).move(ZCLAMP_PFLEX_POS)
    anchor3 = gf.Component()
    anchor3 << gf.components.rectangle(
        size=ZCLAMP_PFLEX_ANCHOR_SIZE, layer=LAYERS.DEVICE_P3, centered=False
    )
    (anchor3 << via(LAYERS.DEVICE_P3)).move(
        (ZCLAMP_PFLEX_ANCHOR_SIZE[0] / 2, ZCLAMP_PFLEX_ANCHOR_SIZE[1] / 2)
    )
    anchor3.move(
        (
            ZCLAMP_PFLEX_POS[0],
            ZCLAMP_PFLEX_POS[1] + ZCLAMP_PFLEX_BAR_LENGTH / 2 - ZCLAMP_PFLEX_BEAM_WIDTH,
        )
    )
    c << anchor3
    (c << anchor3).mirror_y(ZCLAMP_PFLEX_POS[1])

    # Generate peck and carriage
    x0 = ZCLAMP_POS[0] + ZCLAMP_LENGTH1 + ZCLAMP_LENGTH2 - ZCLAMP_PECK_WIDTH
    y0 = (
        (ZCLAMP_PFLEX_BEAM_POS[2] - 0.5) * ZCLAMP_PFLEX_BAR_LENGTH
        + ZCLAMP_PFLEX_POS[1]
        + ZCLAMP_PFLEX_BEAM_WIDTH / 2
    )

    y1 = y0 - ZCLAMP_CARRIAGE_SPACING - ZCLAMP_PFLEX_POS[1]
    x2 = -ZCLAMP_PFLEX_BEAM_LENGTH + ZCANT_CLEARANCE
    y2 = y1 - ZCLAMP_CARRIAGE_WIDTH
    x3 = x2 + ZCLAMP_PFLEX_POS[0] + ZCLAMP_CARRIAGE_WIDTH + ZCANT_CLEARANCE
    y3 = y2 + ZCLAMP_PFLEX_POS[1] - ZCLAMP_COMB_HEIGHT
    y4 = y3 - ZCLAMP_COMB_ANCHOR_WIDTH
    x4 = ZCLAMP_POS[0] + ZCLAMP_LENGTH1 + ZCLAMP_LENGTH2

    peck = c << gl.basic.rectangle(
        size=(
            ZCLAMP_PECK_WIDTH,
            ZCLAMP_PECK_OVERLAP + ZCLAMP_POS[1] - y0,
        ),
        centered=False,
        geometry_layer=LAYERS.DEVICE_P3,
        release_spec=RELEASE_SPEC,
    )

    peck.move((x0, y0))

    peck2 = c << gl.basic.rectangle(
        size=(
            ZCLAMP_POS[0]
            + ZCLAMP_LENGTH1
            + ZCLAMP_LENGTH2
            - ZCLAMP_PFLEX_POS[0]
            - ZCLAMP_CARRIAGE_WIDTH,
            y0 - y2 - ZCLAMP_PFLEX_POS[1],
        ),
        centered=False,
        geometry_layer=LAYERS.DEVICE_P3,
        release_spec=RELEASE_SPEC,
    )
    peck2.move((ZCLAMP_PFLEX_POS[0] + ZCLAMP_CARRIAGE_WIDTH, y2 + ZCLAMP_PFLEX_POS[1]))

    carriage_half = gf.Component()
    (
        carriage_half
        << gl.basic.rectangle(
            size=(
                ZCLAMP_CARRIAGE_WIDTH,
                ZCLAMP_CARRIAGE_SPACING,
            ),
            centered=False,
            geometry_layer=LAYERS.DEVICE_P3,
            release_spec=RELEASE_SPEC,
        )
    ).movey(y1)

    (
        carriage_half
        << gl.basic.rectangle(
            size=(-x2 + ZCLAMP_CARRIAGE_WIDTH, ZCLAMP_CARRIAGE_WIDTH),
            centered=False,
            geometry_layer=LAYERS.DEVICE_P3,
            release_spec=RELEASE_SPEC,
        )
    ).move((x2, y2))

    (
        carriage_half
        << gl.basic.rectangle(
            size=(ZCLAMP_CARRIAGE_WIDTH, y2),
            centered=False,
            geometry_layer=LAYERS.DEVICE_P3,
            release_spec=RELEASE_SPEC,
        )
    ).movex(x2)

    (
        carriage_half
        << gl.basic.rectangle(
            size=(
                x0
                + ZCLAMP_PECK_WIDTH
                - ZCLAMP_PFLEX_POS[0]
                - x2
                - ZCLAMP_CARRIAGE_WIDTH
                - ZCLAMP_CARRIAGE_SPACING,
                ZCLAMP_CARRIAGE_WIDTH,
            ),
            centered=False,
            geometry_layer=LAYERS.DEVICE_P3,
            release_spec=RELEASE_SPEC,
        )
    ).move((x2 + ZCLAMP_CARRIAGE_WIDTH, 0))

    (c << carriage_half).move(ZCLAMP_PFLEX_POS)
    (c << carriage_half).move(ZCLAMP_PFLEX_POS).mirror_y(ZCLAMP_PFLEX_POS[1])

    # Generate combs
    comb_drive = gf.Component()
    comb1 = comb_drive << gl.actuator.comb(
        comb_height=ZCLAMP_COMB_HEIGHT,
        comb_width=ZCLAMP_COMB_WIDTH,
        comb_gap=ZCLAMP_COMB_GAP,
        comb_count=ZCLAMP_COMB_COUNT,
        comb_overlap=ZCLAMP_COMB_OVERLAP,
        geometry_layer=LAYERS.DEVICE_P3,
    )
    comb1.move((x3, y3))

    (
        comb_drive
        << gf.components.rectangle(
            size=(x4 - x3, ZCLAMP_COMB_ANCHOR_WIDTH),
            centered=False,
            layer=LAYERS.DEVICE_P3,
        )
    ).move((x3, y4))

    (c << comb_drive)
    dy = y2 + ZCLAMP_CARRIAGE_WIDTH
    (c << comb_drive).movey(-dy)

    (
        c
        << gf.components.rectangle(
            size=(ZCLAMP_COMB_ANCHOR_WIDTH, dy + ZCLAMP_COMB_ANCHOR_WIDTH),
            centered=False,
            layer=LAYERS.DEVICE_P3,
        )
    ).move((x4, y4 - dy))

    # Connect to bonding pad
    p1 = (x4, y4 - dy + ZCLAMP_COMB_ANCHOR_WIDTH / 2)
    p2 = (CHIP_SIZE / 2 - WIRE_BOND_OFFSET - WIRE_BOND_SIZE / 2, WIRE_BOND_POS[0])
    pmid = (p2[0], p1[1])
    path = gf.path.smooth(
        points=np.array([p1, pmid, p2]),
        radius=ELEC_ROUTING_WIDTH / 2,
    )
    (c << path.extrude(layer=LAYERS.DEVICE_P3_NOISO, width=ELEC_ROUTING_WIDTH))

    # For test only
    # _ = c << gl.basic.rectangle(
    #     size=(
    #         ZCLAMP_PECK_WIDTH,
    #         ZCLAMP_PECK_WIDTH,
    #     ),
    #     centered=False,
    #     geometry_layer=LAYERS.DEVICE_P3,
    #     release_spec=None,
    # )

    # _.move((x0, ZCLAMP_PECK_OVERLAP + ZCLAMP_POS[1]))

    return c


def handle_split():
    c = gf.Component()

    c << gl.basic.ring(
        radius_inner=RDRIVE_MID_RADIUS + CAVITY_WIDTH / 2,
        radius_outer=ZSTAGE_OUTER_RADIUS - ZCANT_ROUTING_CLEARANCE - ELEC_ROUTING_WIDTH,
        angles=(90 - HANDLE_DEVICE_SUPPORT_ANGLE, 90 + HANDLE_DEVICE_SUPPORT_ANGLE),
        geometry_layer=LAYERS.DEVICE_P7,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )

    via_radius = (
        RDRIVE_MID_RADIUS
        + CAVITY_WIDTH / 2
        + ZSTAGE_OUTER_RADIUS
        - ZCANT_ROUTING_CLEARANCE
        - ELEC_ROUTING_WIDTH
    ) / 2
    via_angle_rad = 5 / 180 * np.pi
    (c << via(LAYERS.DEVICE_P7_NOISO)).move(
        (via_radius * np.sin(via_angle_rad), via_radius * np.cos(via_angle_rad))
    )
    (c << via(LAYERS.DEVICE_P7_NOISO)).move(
        (-via_radius * np.sin(via_angle_rad), via_radius * np.cos(via_angle_rad))
    )

    # Make the cuts
    angle_span = CAVITY_WIDTH / RDRIVE_MID_RADIUS * 180 / np.pi
    cut = gl.basic.ring(
        radius_inner=RDRIVE_MID_RADIUS,
        radius_outer=ZSTAGE_OUTER_RADIUS
        + gl.utils.sagitta_offset_safe(
            radius=ZSTAGE_OUTER_RADIUS,
            chord=0,
            angle_resolution=ANGLE_RESOLUTION,
        ),
        angles=(
            90 - HANDLE_SPLIT_ANGLE - angle_span / 2,
            90 - HANDLE_SPLIT_ANGLE + angle_span / 2,
        ),
        geometry_layer=LAYERS.HANDLE_REMOVE,
        angle_resolution=ANGLE_RESOLUTION,
        release_spec=None,
    )
    (c << cut)
    (c << cut).mirror_x()

    return c


def bonding_pads() -> gf.Component:
    c = gf.Component()
    pad = gf.components.rectangle(
        size=(WIRE_BOND_SIZE, WIRE_BOND_SIZE),
        centered=True,
        layer=LAYERS.DEVICE_P3,
    )
    v = via(LAYERS.DEVICE_P3)

    for i, x in enumerate(WIRE_BOND_POS):
        (c << pad).move((x, -CHIP_SIZE / 2 + WIRE_BOND_SIZE / 2 + WIRE_BOND_OFFSET))

        if i in WIRE_BOND_GROUNDED_INDICES:
            for dx in [-0.25, 0.25]:
                for dy in [-0.25, 0.25]:
                    (c << v).move(
                        (
                            x + dx * WIRE_BOND_SIZE,
                            -CHIP_SIZE / 2
                            + WIRE_BOND_SIZE / 2
                            + WIRE_BOND_OFFSET
                            + dy * WIRE_BOND_SIZE,
                        )
                    )

    return c


def chip_label():
    c = gf.Component()

    c << gf.components.rectangle(
        size=LABEL_REGION_SIZE, centered=True, layer=LAYERS.DEVICE_P3
    )

    for ypos, text in LABELS.items():
        c << gf.components.text(
            text=text,
            size=LABEL_TEXT_SIZE,
            position=(0, ypos),
            justify="center",
            layer=LAYERS.DEVICE_REMOVE,
        )
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

    zct = z_cant()
    zact = z_actuator()
    zcl = z_clamp()
    pad = bonding_pads()

    for angle in [0, 90, 180, 270]:
        (c << zct).rotate(angle)
        (c << zact).rotate(angle)
        (c << zcl).rotate(angle)
        (c << pad).rotate(angle)

    label = c << chip_label()
    label.move(LABEL_POSITION)

    c << handle_split()

    return c
