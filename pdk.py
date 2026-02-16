import gdsfactory as gf


class LAYERS(gf.technology.LayerMap):
    DUMMY: gf.typings.Layer = (0, 0)
    DEVICE: gf.typings.Layer = (1, 0)
    DEVICE_P0: gf.typings.Layer = (3, 0)  # Highest priority (front)
    DEVICE_P1: gf.typings.Layer = (3, 1)
    DEVICE_P2: gf.typings.Layer = (3, 2)
    DEVICE_P3: gf.typings.Layer = (3, 3)
    DEVICE_P4: gf.typings.Layer = (3, 4)
    DEVICE_P5: gf.typings.Layer = (3, 5)
    DEVICE_P6: gf.typings.Layer = (3, 6)
    DEVICE_P7: gf.typings.Layer = (3, 7)  # Lowest priority (back)
    DEVICE_REMOVE: gf.typings.Layer = (2, 0)

    # No isolation
    DEVICE_P0_NOISO: gf.typings.Layer = (3, 10)  # Highest priority (front)
    DEVICE_P1_NOISO: gf.typings.Layer = (3, 11)
    DEVICE_P2_NOISO: gf.typings.Layer = (3, 12)
    DEVICE_P3_NOISO: gf.typings.Layer = (3, 13)
    DEVICE_P4_NOISO: gf.typings.Layer = (3, 14)
    DEVICE_P5_NOISO: gf.typings.Layer = (3, 15)
    DEVICE_P6_NOISO: gf.typings.Layer = (3, 16)
    DEVICE_P7_NOISO: gf.typings.Layer = (3, 17)  # Lowest priority (back)

    HANDLE_P0: gf.typings.Layer = (11, 0)  # Highest priority (front)
    HANDLE_P1: gf.typings.Layer = (11, 1)
    HANDLE_P2: gf.typings.Layer = (11, 2)
    HANDLE_P3: gf.typings.Layer = (11, 3)
    HANDLE_P4: gf.typings.Layer = (11, 4)
    HANDLE_P5: gf.typings.Layer = (11, 5)
    HANDLE_P6: gf.typings.Layer = (11, 6)
    HANDLE_P7: gf.typings.Layer = (11, 7)  # Lowest priority (back)
    HANDLE_REMOVE: gf.typings.Layer = (12, 0)

    HANDLE_STEP_ETCH: gf.typings.Layer = (13, 0)

    VIAS_ETCH: gf.typings.Layer = (21, 0)

    TIP0: gf.typings.Layer = (22, 0)
    TIP1: gf.typings.Layer = (22, 1)
    TIP2: gf.typings.Layer = (22, 2)
    TIP3: gf.typings.Layer = (22, 3)


LAYER_VIEWS = gf.technology.LayerViews(filepath="mega2d.yaml")
LAYER_VIEWS.to_lyp("mega2d.lyp")

PDK = gf.Pdk(
    name="mega_2d",
    layers=LAYERS,
    layer_views=LAYER_VIEWS,
)

if __name__ == "__main__":

    # This is a helper function that creates a gdsfactory component specifically designed to visualize the entire layer set.
    # It draws a series of labeled, colored boxes, with each box representing a different layer from the PDK.
    PDK.activate()
    c = LAYER_VIEWS.preview_layerset()
    c.show()
