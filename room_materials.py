"""
room_materials.py -- Material creation and assignment for the Cosy Bedroom Generator.
=====================================================================================
DIGM 131 - Week 9 | Author: Asya Hatice Cag | Drexel University

Contains material utility functions used by the Cosy Bedroom Generator.

This module is responsible for creating Lambert shaders and assigning them
to room geometry. Material logic is kept separate from geometry creation,
JSON handling, and UI code to maintain a modular project structure.

Week 9 updates:
  - Material assignment now supports grouped furniture.
  - Materials are assigned to mesh shapes rather than transform groups.
  - Added validation and defensive error handling.
  - Supports the data-driven room generation workflow in Main.py.
"""


import maya.cmds as cmds


# DEBUG flag
DEBUG = False


def create_material(name, color=(0.5, 0.5, 0.5)):
    """Create a Lambert shader with a specified RGB color.

    If a shader with the requested name already exists, the existing
    shader is returned instead of creating a duplicate.

    Color values are validated and clamped into the valid Maya range
    of 0.0 to 1.0 before the shader is created.

    Args:
        name (str): Name of the shader node.
        color (tuple): RGB color values as (R, G, B).

    Returns:
        str or None: Name of the created shader node, or None if
        shader creation fails.
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
    """Assign a shader to an object, mesh, transform, or furniture group.

    The function supports both single mesh objects and grouped furniture.
    If a group is provided, the hierarchy is searched recursively to find
    all mesh shapes contained within that group.

    Materials are assigned directly to mesh shapes rather than transform
    nodes because Maya only supports material assignment on geometry.

    Args:
        obj_name (str): Name of the object, transform, or group.
        shader_name (str): Name of the shader returned by
            create_material().

    Returns:
        None

    Side Effects:
        - Searches the object hierarchy for mesh shapes.
        - Assigns the specified shader to all discovered mesh shapes.
        - Issues Maya warnings if objects, shaders, or mesh shapes
          cannot be found.
    """


    if not obj_name or not shader_name:
        cmds.warning("[assign_material] Missing object or shader.")
        return

    if not cmds.objExists(obj_name):
        cmds.warning("[assign_material] Object '{}' not found.".format(obj_name))
        return

    if not cmds.objExists(shader_name):
        cmds.warning("[assign_material] Shader '{}' not found.".format(shader_name))
        return

    sg_list = cmds.listConnections(
        "{}.outColor".format(shader_name),
        type="shadingEngine"
    ) or []

    if not sg_list:
        cmds.warning("[assign_material] No shading group for '{}'.".format(shader_name))
        return

    shading_group = sg_list[0]
    mesh_shapes = []

    # Check if the object itself is a mesh shape
    if cmds.nodeType(obj_name) == "mesh":
        mesh_shapes.append(obj_name)

    # Check direct shapes under the object
    direct_shapes = cmds.listRelatives(
        obj_name,
        shapes=True,
        fullPath=True
    ) or []

    for shape in direct_shapes:
        if cmds.nodeType(shape) == "mesh":
            mesh_shapes.append(shape)

    # Check everything under the group
    descendants = cmds.listRelatives(
        obj_name,
        allDescendents=True,
        fullPath=True
    ) or []

    for child in descendants:
        if cmds.nodeType(child) == "mesh":
            mesh_shapes.append(child)

        child_shapes = cmds.listRelatives(
            child,
            shapes=True,
            fullPath=True
        ) or []

        for shape in child_shapes:
            if cmds.nodeType(shape) == "mesh":
                mesh_shapes.append(shape)

    mesh_shapes = list(set(mesh_shapes))

    if not mesh_shapes:
        cmds.warning("[assign_material] No mesh shapes found under '{}'.".format(obj_name))
        print("Children found under '{}': {}".format(
            obj_name,
            cmds.listRelatives(obj_name, allDescendents=True) or []
        ))
        return

    cmds.sets(
        mesh_shapes,
        edit=True,
        forceElement=shading_group
    )

    print("[assign_material] Assigned '{}' to {} mesh shape(s) under '{}'.".format(
        shader_name,
        len(mesh_shapes),
        obj_name
    ))