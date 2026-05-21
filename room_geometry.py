"""
room_geometry.py -- Geometry builders for the Cosy Bedroom Room.
==============================================================
DIGM 131 - Week 7 | Author: Asya Hatice Cag | Drexel University

Week 7 upgrades:
  - DEBUG flag: set to False to silence all [DEBUG] print lines
  - Input validation: negative/zero dimensions replaced with defaults + warning
  - try/except around every cmds call; returns None on failure instead of crashing

Each function creates one type of room element and returns
the Maya node name (or None if something went wrong).

Usage:
    import room_geometry as geo
    geo.create_desk(width=3.5, height=1.5, position=(-3, 0, -2))
"""

import maya.cmds as cmds

# DEBUG flag
DEBUG = True


# Internal helpers


def _positive(value, default, label):
    """Return value if it is strictly positive, else warn and return default.

    Args:
        value  (float): The value to check.
        default (float): Fallback if value <= 0.
        label  (str):   Human-readable name for the warning message.

    Returns:
        float: A positive number guaranteed to be safe for polyCube/polyPlane.
    """
    if value <= 0:
        cmds.warning(
            "[room_geometry] Invalid {} '{}' -- using default {}.".format(
                label, value, default
            )
        )
        return default
    return value


# Room Shell

def create_floor(width=12, depth=12, position=(0, 0, 0)):
    """Create a flat floor plane sitting at y=0.

    Args:
        width    (float): Floor width along X. Default 12.
        depth    (float): Floor depth along Z. Default 12.
        position (tuple): (x, y, z) centre. Default origin.

    Returns:
        str or None: Name of the created floor transform node.
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
        cmds.move(position[0], position[1], position[2], floor)
    except Exception as err:
        cmds.warning("[create_floor] Failed: {}".format(err))
        return None

    return floor


def create_wall(width=12, height=5, axis="x", position=(0, 0, 0)):
    """Create a thin wall panel oriented along the given axis.

    Args:
        width    (float): Length of the wall. Default 12.
        height   (float): Height of the wall. Default 5.
        axis     (str):   'x' for back wall; 'z' for side wall. Default 'x'.
        position (tuple): (x, y, z) centre of the wall. Default origin.

    Returns:
        str or None: Name of the created wall transform node.
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
        cmds.move(position[0], position[1] + height / 2.0, position[2], wall)
    except Exception as err:
        cmds.warning("[create_wall] Failed: {}".format(err))
        return None

    return wall


# Furniture


def create_desk(width=3.5, depth=1.5, height=1.5, position=(0, 0, 0)):
    """Create a desk with a tabletop slab on four legs.

    The desk base sits on y=0 so it rests naturally on the floor.

    Args:
        width (float): Desk width along X. Default 3.5.
        depth (float): Desk depth along Z. Default 1.5.
        height (float): Height from ground to top surface. Default 1.5.
        position (tuple): (x, y, z) base centre of the desk. Default origin.

    Returns:
        str: Name of the desk group transform node.
    """
    if DEBUG:  # FIXED: was 1 space, now correctly 4 spaces
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
        cmds.move(0, height - top_t / 2.0, 0, top)
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
            cmds.move(lx, leg_h / 2.0, lz, leg)
            parts.append(leg)

        group = cmds.group(parts, name="desk_#")
        cmds.move(position[0], position[1], position[2], group)
    except Exception as err:
        cmds.warning("[create_desk] Failed: {}".format(err))
        return None

    return group


def create_chair(seat_width=0.9, seat_depth=0.9, seat_height=1.0,
                 back_height=0.8, position=(0, 0, 0)):
    """Create a chair with a seat cushion, backrest, and four legs.

    The chair base sits on y=0 so it rests naturally on the floor.

    Args:
        seat_width (float): Width of the seat. Default 0.9.
        seat_depth (float): Depth of the seat. Default 0.9.
        seat_height (float): Height of the seat surface from ground. Default 1.0.
        back_height (float): Height of the backrest above the seat. Default 0.8.
        position (tuple): (x, y, z) base centre. Default origin.

    Returns:
        str: Name of the chair group transform node.
    """
    if DEBUG:
        print("[DEBUG] create_chair: sw={}, sd={}, sh={}, bh={}, pos={}".format(
            seat_width, seat_depth, seat_height, back_height, position))

    seat_width  = _positive(seat_width,  0.9, "seat_width")
    seat_depth  = _positive(seat_depth,  0.9, "seat_depth")
    seat_height = _positive(seat_height, 1.0, "seat_height")
    back_height = _positive(back_height, 0.8, "back_height")

    try:
        parts = []
        seat_t = 0.1
        leg_h  = seat_height - seat_t

        seat = cmds.polyCube(
            name="seat_#", width=seat_width, height=seat_t, depth=seat_depth,
        )[0]
        cmds.move(0, seat_height, 0, seat)
        parts.append(seat)

        back = cmds.polyCube(
            name="backrest_#", width=seat_width, height=back_height, depth=seat_t,
        )[0]
        cmds.move(
            0,
            seat_height + back_height / 2.0,
            -(seat_depth / 2.0 - seat_t / 2.0),
            back,
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
            cmds.move(lx, leg_h / 2.0, lz, leg)
            parts.append(leg)

        group = cmds.group(parts, name="chair_#")
        cmds.move(position[0], position[1], position[2], group)
    except Exception as err:
        cmds.warning("[create_chair] Failed: {}".format(err))
        return None

    return group


def create_bookshelf(width=1.2, height=3.5, depth=0.4, shelves=4, position=(0, 0, 0)):
    """Create a bookshelf with two side panels, a back panel, and shelf boards.

    The bookshelf base sits on y=0 so it rests naturally on the floor.

    Args:
        width (float): Overall width along X. Default 1.2.
        height (float): Overall height. Default 3.5.
        depth (float): Overall depth along Z. Default 0.4.
        shelves (int): Number of horizontal shelf boards. Default 4.
        position (tuple): (x, y, z) base centre. Default origin.

    Returns:
        str: Name of the bookshelf group transform node.
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
            cmds.move(side_x, height / 2.0, 0, panel)
            parts.append(panel)

        back = cmds.polyCube(
            name="shelf_back_#", width=width, height=height, depth=pt,
        )[0]
        cmds.move(0, height / 2.0, -depth / 2.0 + pt / 2.0, back)
        parts.append(back)

        for i in range(shelves):
            # FIXED: was dividing by (shelves - 1) causing ZeroDivisionError when shelves == 1
            shelf_y = (i * height / (shelves - 1)) if shelves > 1 else (height / 2.0)
            board = cmds.polyCube(
                name="shelf_board_#",
                width=width - pt * 2,
                height=pt,
                depth=depth,
            )[0]
            cmds.move(0, shelf_y + pt / 2.0, 0, board)
            parts.append(board)

        group = cmds.group(parts, name="bookshelf_#")
        cmds.move(position[0], position[1], position[2], group)
    except Exception as err:
        cmds.warning("[create_bookshelf] Failed: {}".format(err))
        return None

    return group


def create_bed(width=2.2, length=3.5, height=0.6, position=(0, 0, 0)):
    """Create a bed with a base frame and a mattress block on top.

    The bed base sits on y=0 so it rests naturally on the floor.

    Args:
        width (float): Bed width along X. Default 2.2.
        length (float): Bed length along Z. Default 3.5.
        height (float): Height of the bed frame. Default 0.6.
        position (tuple): (x, y, z) base centre of the bed. Default origin.

    Returns:
        str: Name of the bed group transform node.
    """
    if DEBUG:
        print("[DEBUG] create_bed: width={}, length={}, height={}, pos={}".format(
            width, length, height, position))

    width  = _positive(width,  2.2, "bed width")
    length = _positive(length, 3.5, "bed length")
    height = _positive(height, 0.6, "bed height")

    try:
        parts = []
        frame_t    = 0.1
        mattress_h = 0.25

        frame = cmds.polyCube(
            name="bed_frame_#", width=width, height=height, depth=length,
        )[0]
        cmds.move(0, height / 2.0, 0, frame)
        parts.append(frame)

        mattress = cmds.polyCube(
            name="mattress_#",
            width=width - frame_t * 2,
            height=mattress_h,
            depth=length - frame_t * 2,
        )[0]
        cmds.move(0, height + mattress_h / 2.0, 0, mattress)
        parts.append(mattress)

        headboard = cmds.polyCube(
            name="headboard_#", width=width, height=height * 1.5, depth=frame_t,
        )[0]
        cmds.move(0, height * 0.75, -(length / 2.0 - frame_t / 2.0), headboard)
        parts.append(headboard)

        group = cmds.group(parts, name="bed_#")
        cmds.move(position[0], position[1], position[2], group)
    except Exception as err:
        cmds.warning("[create_bed] Failed: {}".format(err))
        return None

    return group


def create_couch(width=2.8, depth=1.0, seat_height=0.5,
                 back_height=0.7, position=(0, 0, 0)):
    """Create a couch with a seat, backrest, and two armrests.

    The couch base sits on y=0 so it rests naturally on the floor.

    Args:
        width (float): Couch width along X. Default 2.8.
        depth (float): Couch depth along Z. Default 1.0.
        seat_height (float): Height of the seat surface. Default 0.5.
        back_height (float): Height of the backrest above the seat. Default 0.7.
        position (tuple): (x, y, z) base centre. Default origin.

    Returns:
        str: Name of the couch group transform node.
    """
    if DEBUG:  # FIXED: was 3 spaces, now correctly 4 spaces
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
        cmds.move(0, base_h / 2.0, 0, base)
        parts.append(base)

        seat = cmds.polyCube(
            name="couch_seat_#", width=width - arm_t * 2, height=seat_t, depth=depth,
        )[0]
        cmds.move(0, seat_height, 0, seat)
        parts.append(seat)

        back = cmds.polyCube(
            name="couch_back_#", width=width, height=back_height, depth=back_t,
        )[0]
        cmds.move(
            0,
            seat_height + back_height / 2.0,
            -(depth / 2.0 - back_t / 2.0),
            back,
        )
        parts.append(back)

        for side_x in [-width / 2.0 + arm_t / 2.0, width / 2.0 - arm_t / 2.0]:
            arm = cmds.polyCube(
                name="couch_arm_#",
                width=arm_t,
                height=seat_height + seat_t * 1.5,
                depth=depth,
            )[0]
            cmds.move(side_x, (seat_height + seat_t * 1.5) / 2.0, 0, arm)
            parts.append(arm)

        group = cmds.group(parts, name="couch_#")
        cmds.move(position[0], position[1], position[2], group)
    except Exception as err:
        cmds.warning("[create_couch] Failed: {}".format(err))
        return None

    return group


# Self-test


if __name__ == "__main__":
    cmds.file(new=True, force=True)

    create_floor(position=(0, 0, 0))
    create_wall(axis="x", position=(0, 0, -6))
    create_wall(axis="z", position=(-6, 0, 0))
    create_desk(position=(-3, 0, -2))
    create_chair(position=(-3, 0, -0.5))
    create_bookshelf(position=(3, 0, -4))
    create_bed(position=(2, 0, 2))
    create_couch(position=(0, 0, 3))

    cmds.viewFit(allObjects=True)
    print("room_geometry self-test complete!")