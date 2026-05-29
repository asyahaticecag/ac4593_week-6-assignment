"""
room_materials.py -- Material creation and assignment for the Cosy Bedroom Room.
===============================================================================
DIGM 131 - Week 8 | Author: Asya Hatice Cag | Drexel University

Week 7 upgrades:
  - DEBUG flag for print-based tracing
  - Input validation: color channels clamped to [0, 1] with warnings
  - try/except around all cmds calls

Week 8 fix:
  - noSurfaceShader=True was preventing the SG from accepting a surface shader.
    Changed to noSurfaceShader=False so Lambert color actually shows in viewport.

Usage:
    import room_materials as mat
    wood = mat.create_material("warm_wood", (0.55, 0.38, 0.22))
    mat.assign_material("desk_1", wood)
"""

import maya.cmds as cmds


# DEBUG flag
DEBUG = False


def create_material(name, color=(0.5, 0.5, 0.5)):
    """Create a Lambert shader with the given name and RGB color.

    If a shader with this name already exists, return it without creating
    a duplicate. Each channel is clamped to [0, 1] with a warning if out
    of range.

    Args:
        name  (str):   Name for the shader node.
        color (tuple): (R, G, B) floats, each 0.0 to 1.0.

    Returns:
        str or None: The name of the shader node, or None on failure.
    """
    if DEBUG:
        print("[DEBUG] create_material: name='{}', color={}".format(name, color))

    # Validate and clamp color channels
    clamped = []
    for i, channel in enumerate(color):
        if channel < 0.0 or channel > 1.0:
            cmds.warning(
                "[create_material] Color channel {} value '{}' out of [0,1] "
                "-- clamping.".format(i, channel)
            )
            channel = max(0.0, min(1.0, channel))
        clamped.append(channel)
    color = tuple(clamped)

    if cmds.objExists(name):
        return name

    try:
        shader = cmds.shadingNode("lambert", asShader=True, name=name)
        sg = cmds.sets(
            renderable=True, noSurfaceShader=False,
            empty=True, name="{}_SG".format(name),
        )
        cmds.connectAttr(
            "{}.outColor".format(shader),
            "{}.surfaceShader".format(sg),
            force=True,
        )
        cmds.setAttr("{}.color".format(shader), *color, type="double3")
    except Exception as err:
        cmds.warning("[create_material] Failed to create '{}': {}".format(name, err))
        return None

    return shader


def assign_material(obj_name, shader_name):
    """Assign a shader to a Maya object or group.

    Handles groups by finding all descendant shapes automatically.

    Args:
        obj_name    (str): Transform, shape, or group node name.
        shader_name (str): Shader node name returned by create_material.
    """
    if DEBUG:
        print("[DEBUG] assign_material: obj='{}', shader='{}'".format(
            obj_name, shader_name))

    if not obj_name or not shader_name:
        cmds.warning("[assign_material] Received None argument -- skipping.")
        return

    if not cmds.objExists(obj_name):
        cmds.warning(
            "[assign_material] Object '{}' not found -- skipping.".format(obj_name)
        )
        return

    if not cmds.objExists(shader_name):
        cmds.warning(
            "[assign_material] Shader '{}' not found -- skipping.".format(shader_name)
        )
        return

    try:
        sg_list = cmds.listConnections(
            "{}.outColor".format(shader_name),
            type="shadingEngine"
        )

        if not sg_list:
            cmds.warning(
                "[assign_material] No shading group for '{}' -- skipping.".format(
                    shader_name
                )
            )
            return

        # Collect ALL mesh shapes under this node (direct + all descendants).
        # Maya can only assign materials to mesh shapes, never to transforms
        # or group nodes, so we must walk the full hierarchy.
        all_shapes = cmds.listRelatives(
            obj_name,
            allDescendents=True,
            shapes=True,
            fullPath=True,
            type="mesh",       # mesh only — skips cameras, lights, etc.
        ) or []

        # Also grab any direct mesh shapes (handles single-mesh objects)
        direct_shapes = cmds.listRelatives(
            obj_name,
            shapes=True,
            fullPath=True,
            type="mesh",
        ) or []

        targets = list(set(all_shapes + direct_shapes))

        if not targets:
            cmds.warning(
                "[assign_material] No mesh shapes found under '{}'".format(obj_name)
            )
            return

        if DEBUG:
            print("[DEBUG] assign_material: assigning '{}' to {} shapes under '{}'".format(
                shader_name, len(targets), obj_name))

        cmds.sets(
            targets,
            edit=True,
            forceElement=sg_list[0]
        )

    except Exception as err:
        cmds.warning(
            "[assign_material] Failed assigning '{}' to '{}': {}".format(
                shader_name,
                obj_name,
                err
            )
        )

