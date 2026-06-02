"""
room_geometry.py -- Geometry builders for the Cosy Bedroom Generator.
====================================================================
DIGM 131 - Week 9 | Author: Asya Hatice Cag | Drexel University

Contains the geometry-building functions for the Cosy Bedroom Generator.
Each function creates one room or furniture element using Maya primitives,
groups multi-part furniture, moves the finished object into position, and
returns the created transform node.

This file only handles geometry. It does not assign materials, save JSON,
or create UI controls. Those responsibilities are handled by separate modules.

Week 9 updates:
  - Geometry functions remain separated from UI and JSON logic.
  - Builder functions support the data-driven ROOM_CONFIG system in Main.py.
  - Multi-part furniture returns a group node so materials and transforms can
    be applied from the driver loop.
  - Input validation and try/except protection remain in place for safer builds.
"""


import maya.cmds as cmds

# DEBUG flag
DEBUG = False


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _positive(value, default, label):
    """Validate that a numeric value is positive.

    If the value is zero or negative, the function warns the user and
    returns a safe default. This prevents Maya primitive commands from
    receiving invalid dimensions.

    Args:
        value (float): Value to check.
        default (float): Safe fallback value.
        label (str): Name of the value being checked, used in warnings.

    Returns:
        float: The original value if valid, otherwise the default value.
    """
    if value <= 0:
        cmds.warning(
            "[room_geometry] Invalid {} '{}' -- using default {}.".format(
                label, value, default
            )
        )
        return default
    return value


# ---------------------------------------------------------------------------
# Room Shell
# ---------------------------------------------------------------------------

def create_floor(width=12, depth=12, position=(0, 0, 0)):
    """Create the bedroom floor.

    Builds a flat polygon plane at the requested position. The floor acts
    as the base surface for the full bedroom layout.

    Args:
        width (float): Size of the floor along the X axis.
        depth (float): Size of the floor along the Z axis.
        position (tuple): World-space center position as (x, y, z).

    Returns:
        str or None: Floor transform node name, or None if creation fails.
    """
    if DEBUG:
        print("[DEBUG] create_floor: width={}, depth={}, pos={}".format(width, depth, position))

    width = _positive(width, 12, "floor width")
    depth = _positive(depth, 12, "floor depth")

    try:
        floor = cmds.polyPlane(
            name="floor_#",
            width=width,
            height=depth,
            subdivisionsX=1,
            subdivisionsY=1,
        )[0]
        cmds.move(position[0], position[1], position[2], floor, worldSpace=True)
    except Exception as err:
        cmds.warning("[create_floor] Failed: {}".format(err))
        return None

    return floor


def create_wall(width=12, height=5, axis="x", position=(0, 0, 0)):
    """Create a room wall panel.

    Builds a thin polygon cube wall. The axis value controls whether the
    wall stretches across the X axis or the Z axis.

    Args:
        width (float): Length of the wall.
        height (float): Height of the wall.
        axis (str): "x" creates a back/front wall, "z" creates a side wall.
        position (tuple): Base-center world position as (x, y, z).

    Returns:
        str or None: Wall transform node name, or None if creation fails.
    """
    if DEBUG:
        print("[DEBUG] create_wall: width={}, height={}, axis='{}', pos={}".format(
            width, height, axis, position))

    width  = _positive(width,  12, "wall width")
    height = _positive(height,  5, "wall height")

    try:
        if axis == "x":
            wall = cmds.polyCube(
                name="wall_#", width=width, height=height, depth=0.15,
            )[0]
        else:
            wall = cmds.polyCube(
                name="wall_#", width=0.15, height=height, depth=width,
            )[0]
        cmds.move(position[0], position[1] + height / 2.0, position[2], wall, worldSpace=True)
    except Exception as err:
        cmds.warning("[create_wall] Failed: {}".format(err))
        return None

    return wall


# ---------------------------------------------------------------------------
# Furniture
# ---------------------------------------------------------------------------

def create_desk(width=3.5, depth=1.5, height=1.5, position=(0, 0, 0)):
    """Create a desk from simple polygon pieces.

    Builds a tabletop and four legs, groups the pieces, and moves the
    finished desk into position.

    Args:
        width (float): Desk width along the X axis.
        depth (float): Desk depth along the Z axis.
        height (float): Total desk height from floor to tabletop.
        position (tuple): Base-center world position as (x, y, z).

    Returns:
        str or None: Desk group node name, or None if creation fails.
    """
    if DEBUG:
        print("[DEBUG] create_desk: width={}, depth={}, height={}, pos={}".format(
            width, depth, height, position))

    width  = _positive(width,  3.5, "desk width")
    depth  = _positive(depth,  1.5, "desk depth")
    height = _positive(height, 1.5, "desk height")

    try:
        parts = []
        top_t = 0.1
        leg_h = height - top_t

        top = cmds.polyCube(
            name="desk_top_#", width=width, height=top_t, depth=depth,
        )[0]
        cmds.move(0, height - top_t / 2.0, 0, top, worldSpace=True)
        parts.append(top)

        for lx, lz in [
            ( width / 2.0 - 0.1, -(depth / 2.0 - 0.1)),
            (-width / 2.0 + 0.1, -(depth / 2.0 - 0.1)),
            ( width / 2.0 - 0.1,  (depth / 2.0 - 0.1)),
            (-width / 2.0 + 0.1,  (depth / 2.0 - 0.1)),
        ]:
            leg = cmds.polyCube(
                name="desk_leg_#", width=0.1, height=leg_h, depth=0.1,
            )[0]
            cmds.move(lx, leg_h / 2.0, lz, leg, worldSpace=True)
            parts.append(leg)

        group = cmds.group(parts, name="desk_#")
        cmds.move(position[0], position[1], position[2], group, worldSpace=True)
    except Exception as err:
        cmds.warning("[create_desk] Failed: {}".format(err))
        return None

    return group


def create_chair(seat_width=0.9, seat_depth=0.9, seat_height=1.0,
                 back_height=0.8, position=(0, 0, 0)):
    """Create a chair from simple polygon pieces.

    Builds a seat, backrest, and four legs. The pieces are grouped so the
    driver can move, rotate, and assign materials to the chair as one object.

    Args:
        seat_width (float): Width of the seat along the X axis.
        seat_depth (float): Depth of the seat along the Z axis.
        seat_height (float): Height of the seat from the floor.
        back_height (float): Height of the backrest above the seat.
        position (tuple): Base-center world position as (x, y, z).

    Returns:
        str or None: Chair group node name, or None if creation fails.
    """
    if DEBUG:
        print("[DEBUG] create_chair: sw={}, sd={}, sh={}, bh={}, pos={}".format(
            seat_width, seat_depth, seat_height, back_height, position))

    seat_width  = _positive(seat_width,  0.9, "seat_width")
    seat_depth  = _positive(seat_depth,  0.9, "seat_depth")
    seat_height = _positive(seat_height, 1.0, "seat_height")
    back_height = _positive(back_height, 0.8, "back_height")

    try:
        parts  = []
        seat_t = 0.1
        leg_h  = seat_height - seat_t

        seat = cmds.polyCube(
            name="seat_#", width=seat_width, height=seat_t, depth=seat_depth,
        )[0]
        cmds.move(0, seat_height, 0, seat, worldSpace=True)
        parts.append(seat)

        back = cmds.polyCube(
            name="backrest_#", width=seat_width, height=back_height, depth=seat_t,
        )[0]
        cmds.move(
            0,
            seat_height + back_height / 2.0,
            -(seat_depth / 2.0 - seat_t / 2.0),
            back,
            worldSpace=True,
        )
        parts.append(back)

        for lx, lz in [
            ( seat_width / 2.0 - 0.1,  seat_depth / 2.0 - 0.1),
            (-seat_width / 2.0 + 0.1,  seat_depth / 2.0 - 0.1),
            ( seat_width / 2.0 - 0.1, -seat_depth / 2.0 + 0.1),
            (-seat_width / 2.0 + 0.1, -seat_depth / 2.0 + 0.1),
        ]:
            leg = cmds.polyCube(
                name="chair_leg_#", width=0.08, height=leg_h, depth=0.08,
            )[0]
            cmds.move(lx, leg_h / 2.0, lz, leg, worldSpace=True)
            parts.append(leg)

        group = cmds.group(parts, name="chair_#")
        cmds.move(position[0], position[1], position[2], group, worldSpace=True)
    except Exception as err:
        cmds.warning("[create_chair] Failed: {}".format(err))
        return None

    return group


def create_bookshelf(width=1.2, height=3.5, depth=0.4, shelves=4, position=(0, 0, 0)):
    """Create a bookshelf from side panels and shelf boards.

    Builds two vertical side panels, a back panel, and a configurable number
    of horizontal shelves. The pieces are grouped into one bookshelf object.

    Args:
        width (float): Overall bookshelf width along the X axis.
        height (float): Overall bookshelf height.
        depth (float): Overall bookshelf depth along the Z axis.
        shelves (int): Number of horizontal shelf boards.
        position (tuple): Base-center world position as (x, y, z).

    Returns:
        str or None: Bookshelf group node name, or None if creation fails.
    """
    if DEBUG:
        print("[DEBUG] create_bookshelf: w={}, h={}, d={}, shelves={}, pos={}".format(
            width, height, depth, shelves, position))

    width  = _positive(width,  1.2, "bookshelf width")
    height = _positive(height, 3.5, "bookshelf height")
    depth  = _positive(depth,  0.4, "bookshelf depth")

    if not isinstance(shelves, int) or shelves < 1:
        cmds.warning("[create_bookshelf] Invalid shelves '{}' -- using 4.".format(shelves))
        shelves = 4

    try:
        parts = []
        pt = 0.05

        for side_x in [-width / 2.0 + pt / 2.0, width / 2.0 - pt / 2.0]:
            panel = cmds.polyCube(
                name="shelf_side_#", width=pt, height=height, depth=depth,
            )[0]
            cmds.move(side_x, height / 2.0, 0, panel, worldSpace=True)
            parts.append(panel)

        back = cmds.polyCube(
            name="shelf_back_#", width=width, height=height, depth=pt,
        )[0]
        cmds.move(0, height / 2.0, -depth / 2.0 + pt / 2.0, back, worldSpace=True)
        parts.append(back)

        for i in range(shelves):
            shelf_y = (i * height / (shelves - 1)) if shelves > 1 else (height / 2.0)
            board = cmds.polyCube(
                name="shelf_board_#",
                width=width - pt * 2,
                height=pt,
                depth=depth,
            )[0]
            cmds.move(0, shelf_y + pt / 2.0, 0, board, worldSpace=True)
            parts.append(board)

        group = cmds.group(parts, name="bookshelf_#")
        cmds.move(position[0], position[1], position[2], group, worldSpace=True)
    except Exception as err:
        cmds.warning("[create_bookshelf] Failed: {}".format(err))
        return None

    return group


def create_bed(width=2.2, length=3.5, height=0.6, position=(0, 0, 0)):
    """Create a bed from frame, mattress, and headboard pieces.

    Builds the bed frame first, then adds a mattress and headboard. The
    completed bed is grouped so it can be positioned as one object.

    Args:
        width (float): Bed width along the X axis.
        length (float): Bed length along the Z axis.
        height (float): Height of the bed frame.
        position (tuple): Base-center world position as (x, y, z).

    Returns:
        str or None: Bed group node name, or None if creation fails.
    """
    if DEBUG:
        print("[DEBUG] create_bed: width={}, length={}, height={}, pos={}".format(
            width, length, height, position))

    width  = _positive(width,  2.2, "bed width")
    length = _positive(length, 3.5, "bed length")
    height = _positive(height, 0.6, "bed height")

    try:
        parts      = []
        frame_t    = 0.1
        mattress_h = 0.25

        frame = cmds.polyCube(
            name="bed_frame_#", width=width, height=height, depth=length,
        )[0]
        cmds.move(0, height / 2.0, 0, frame, worldSpace=True)
        parts.append(frame)

        mattress = cmds.polyCube(
            name="mattress_#",
            width=width - frame_t * 2,
            height=mattress_h,
            depth=length - frame_t * 2,
        )[0]
        cmds.move(0, height + mattress_h / 2.0, 0, mattress, worldSpace=True)
        parts.append(mattress)

        headboard = cmds.polyCube(
            name="headboard_#", width=width, height=height * 1.5, depth=frame_t,
        )[0]
        cmds.move(0, height * 0.75, -(length / 2.0 - frame_t / 2.0), headboard, worldSpace=True)
        parts.append(headboard)

        group = cmds.group(parts, name="bed_#")
        cmds.move(position[0], position[1], position[2], group, worldSpace=True)
    except Exception as err:
        cmds.warning("[create_bed] Failed: {}".format(err))
        return None

    return group


def create_couch(width=2.8, depth=1.0, seat_height=0.5,
                 back_height=0.7, position=(0, 0, 0)):
    """Create a couch from simple polygon pieces.

    Builds a couch base, seat cushion, backrest, and two armrests. The pieces
    are grouped so the couch can be moved, rotated, and assigned material as
    one object.

    Args:
        width (float): Couch width along the X axis.
        depth (float): Couch depth along the Z axis.
        seat_height (float): Height of the couch seat.
        back_height (float): Height of the couch backrest.
        position (tuple): Base-center world position as (x, y, z).

    Returns:
        str or None: Couch group node name, or None if creation fails.
    """
    if DEBUG:
        print("[DEBUG] create_couch: w={}, d={}, sh={}, bh={}, pos={}".format(
            width, depth, seat_height, back_height, position))

    width       = _positive(width,       2.8, "couch width")
    depth       = _positive(depth,       1.0, "couch depth")
    seat_height = _positive(seat_height, 0.5, "seat_height")
    back_height = _positive(back_height, 0.7, "back_height")

    try:
        parts  = []
        arm_t  = 0.15
        seat_t = 0.15
        back_t = 0.15
        base_h = seat_height - seat_t

        base = cmds.polyCube(
            name="couch_base_#", width=width, height=base_h, depth=depth,
        )[0]
        cmds.move(0, base_h / 2.0, 0, base, worldSpace=True)
        parts.append(base)

        seat = cmds.polyCube(
            name="couch_seat_#", width=width - arm_t * 2, height=seat_t, depth=depth,
        )[0]
        cmds.move(0, seat_height, 0, seat, worldSpace=True)
        parts.append(seat)

        back = cmds.polyCube(
            name="couch_back_#", width=width, height=back_height, depth=back_t,
        )[0]
        cmds.move(
            0,
            seat_height + back_height / 2.0,
            -(depth / 2.0 - back_t / 2.0),
            back,
            worldSpace=True,
        )
        parts.append(back)

        for side_x in [-width / 2.0 + arm_t / 2.0, width / 2.0 - arm_t / 2.0]:
            arm = cmds.polyCube(
                name="couch_arm_#",
                width=arm_t,
                height=seat_height + seat_t * 1.5,
                depth=depth,
            )[0]
            cmds.move(side_x, (seat_height + seat_t * 1.5) / 2.0, 0, arm, worldSpace=True)
            parts.append(arm)

        group = cmds.group(parts, name="couch_#")
        cmds.move(position[0], position[1], position[2], group, worldSpace=True)
    except Exception as err:
        cmds.warning("[create_couch] Failed: {}".format(err))
        return None

    return group


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    cmds.file(new=True, force=True)

    create_floor(position=(0, 0, 0))
    create_wall(axis="x", position=(0, 0, -6))
    create_wall(axis="z", position=(-6, 0, 0))

    create_desk(position=(-3.85, 0, -4.85))
    create_chair(position=(-3.85, 0, -3.0))
    create_bookshelf(position=(2.5, 0, -5.6))
    create_bed(position=(4.7, 0, -3.85))
    create_couch(position=(0, 0, 4.5))

    cmds.viewFit(allObjects=True)
    print("room_geometry self-test complete!")