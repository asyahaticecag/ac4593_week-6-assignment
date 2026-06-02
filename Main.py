"""
main.py -- Cosy Bedroom Generator
=================================
DIGM 131 - Week 9 | Author: Asya Hatice Cag | Drexel University

Assembles a complete cosy bedroom using separate geometry,
material, JSON, and UI modules. All major scene elements are
defined through ROOM_CONFIG so the room can be edited through
data instead of rewriting the driver loop.

Week 9 updates:
  - Added JSON save/load support through room_io.py.
  - Added Maya UI support through room_ui.py.
  - Added optional rotation support for data-driven layout control.
  - Updated material assignment so shaders work on grouped furniture.
  - Updated room layout with the bed in the corner, desk and chair nearby,
    and chair/couch rotated to face the correct direction.
"""

import os
import sys
import maya.cmds as cmds

# ---------------------------------------------------------------------------
# sys.path block -- lets Maya find sibling modules
# ---------------------------------------------------------------------------
try:
    _THIS_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _THIS_DIR = cmds.workspace(query=True, rootDirectory=True)

if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)


import room_geometry as geo
import room_materials as mat

import importlib
geo = importlib.reload(geo)
mat = importlib.reload(mat)

print("USING ROOM MATERIALS FROM:", mat.__file__)

# DEBUG flag
DEBUG = False

# Material palette:  key -> (shader_name, (R, G, B))
MATERIAL_PALETTE = {
    "floor":     ("pale_wood",    (0.76, 0.64, 0.48)),
    "wall":      ("warm_plaster", (0.92, 0.88, 0.82)),
    "desk":      ("dark_wood",    (0.40, 0.26, 0.14)),
    "chair":     ("mid_wood",     (0.55, 0.38, 0.22)),
    "bookshelf": ("mid_wood",     (0.55, 0.38, 0.22)),
    "bed":       ("soft_linen",   (0.85, 0.82, 0.76)),
    "couch":     ("sage_green",   (0.45, 0.55, 0.45)),
}

# BUILDERS dispatcher -- maps type string to geometry builder function
BUILDERS = {
    "floor":     geo.create_floor,
    "wall":      geo.create_wall,
    "desk":      geo.create_desk,
    "chair":     geo.create_chair,
    "bookshelf": geo.create_bookshelf,
    "bed":       geo.create_bed,
    "couch":     geo.create_couch,
}

# Data-driven room configuration
ROOM_CONFIG = [
    # --- Room shell ---
    {
        "type": "floor",
        "material": "floor",
        "width": 12,
        "depth": 12,
        "position": (0, 0, 0),
    },
    {
        "type": "wall",
        "material": "wall",
        "width": 12,
        "height": 5,
        "axis": "x",
        "position": (0, 0, -6),
    },
    {
        "type": "wall",
        "material": "wall",
        "width": 12,
        "height": 5,
        "axis": "z",
        "position": (-6, 0, 0),
    },

    # --- Furniture ---
    {
        "type": "desk",
        "material": "desk",
        "width": 3.5,
        "depth": 1.5,
        "height": 1.5,
        "position": (0.2, 0, -5.0),
    },
    {
        "type": "chair",
        "material": "chair",
        "seat_width": 0.9,
        "seat_depth": 0.9,
        "seat_height": 1.0,
        "back_height": 0.8,
        "position": (0.2, 0, -3.0),
    },
    {
        "type": "bookshelf",
        "material": "bookshelf",
        "width": 1.2,
        "height": 3.5,
        "depth": 0.4,
        "shelves": 4,
        "position": (2.8, 0, -5.6),
    },
    {
        "type": "bed",
        "material": "bed",
        "width": 2.2,
        "length": 3.5,
        "height": 0.6,
        "position": (-4.7, 0, -4.1),
    },
    {
        "type": "couch",
        "material": "couch",
        "width": 2.8,
        "depth": 1.0,
        "seat_height": 0.5,
        "back_height": 0.7,
        "position": (0, 0, 4.5),
    },
    
    # Aaron's Addition 
    {
    "type": "wall",
    "material": "wall",
    "width": 12,
    "height": 5,
    "axis": "x",
    "position": (0, 0, 6),
    },
    {
    "type": "bookshelf",
    "material": "bookshelf",
    "width": 1.0,
    "height": 3.0,
    "depth": 0.4,
    "shelves": 5,
    "position": (4.9, 0, -5.6),
    },
]


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

def create_element(data):
    """Create one scene element from a ROOM_CONFIG dictionary.

    The function validates the config entry, looks up the matching
    builder function from BUILDERS, removes metadata keys that should
    not be passed into geometry functions, and applies optional rotation
    after the object is created.

    Args:
        data (dict): One dictionary entry from ROOM_CONFIG. Expected keys
            include "type", "material", dimensions, "position", and
            optionally "rotation".

    Returns:
        str or None: Maya node name on success, None if validation or
        construction fails.
    """
    if not isinstance(data, dict):
        cmds.warning(
            "Config entry is not a dictionary."
        )
        return None
    
    # --- Layer 1: check "type" key exists ---
    element_type = data.get("type")
    if not element_type:
        cmds.warning("[create_element] Entry is missing a 'type' key -- skipping: {}".format(data))
        return None

    if DEBUG:
        print("[DEBUG] create_element: dispatching type='{}'".format(element_type))

    # --- Layer 2: look up the builder ---
    builder = BUILDERS.get(element_type)
    if not builder:
        cmds.warning("[create_element] Unknown type '{}' -- skipping.".format(element_type))
        return None

    # --- Strip meta-keys before ** unpacking ---
    params = {k: v for k, v in data.items() if k not in ("type", "material")}

    # --- Layer 3: call the builder ---
    try:
        node = builder(**params)
    except TypeError as err:
        cmds.warning(
            "[create_element] Bad parameters for type '{}': {} -- skipping.".format(
                element_type, err
            )
        )
        return None
    except Exception as err:
        cmds.warning(
            "[create_element] Unexpected error building '{}': {} -- skipping.".format(
                element_type, err
            )
        )
        return None

    if DEBUG:
        print("[DEBUG] create_element: created '{}'".format(node))

    return node


# ---------------------------------------------------------------------------
# Room builder / Driver loop
# ---------------------------------------------------------------------------

def build_room():
    """Build the full cosy bedroom scene.

    Clears the current Maya scene, creates all materials, loops through
    ROOM_CONFIG, builds each room element, applies the matching material,
    and groups the completed objects under one top-level room group.

    Returns:
        str or None: Name of the final cosy bedroom group, or None if no
        parts were created.
    """
    cmds.file(new=True, force=True)

    # Create all material shaders up front
    shaders = {}
    for key, (name, color) in MATERIAL_PALETTE.items():

        shader = mat.create_material(name, color)

        if shader:
            shaders[key] = shader
        else:
            cmds.warning(
                "Material '{}' failed.".format(name)
            )

    parts = []

    # --- Driver loop: iterate config, dispatch each entry ---
    for entry in ROOM_CONFIG:
        node = create_element(entry)
        if node is None:
            continue

        # Apply material
        mat_key = entry.get("material")
        if mat_key and mat_key in shaders:
            mat.assign_material(node, shaders[mat_key])
        elif mat_key:
            cmds.warning(
                "[build_room] Material key '{}' not in palette -- no shader applied.".format(mat_key)
            )

        # Rotate chair 180 degrees
        if entry["type"] == "chair":
            cmds.rotate(0, 180, 0, node, worldSpace=True)

        # Rotate couch 180 degrees
        if entry["type"] == "couch":
            cmds.rotate(0, 180, 0, node, worldSpace=True)

        parts.append(node)

    cmds.viewFit(allObjects=True)
    print("=== Cosy Bedroom Complete ===")
    print("  {} parts assembled from {} config entries.".format(
        len(parts), len(ROOM_CONFIG)
    ))

    if not parts:
        cmds.warning("No room parts were created.")
        return None

    return cmds.group(parts, name="cosy_bedroom_#")


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    build_room()
