# Cosy Bedroom Generator

## What It Does
Generates a cosy bedroom from configuration parameters. The room contains a
desk, chair, bookshelf, bed, and couch, all placed on the floor inside two
corner walls. Every piece of furniture and architecture is described as a
dictionary entry in ROOM_CONFIG inside main.py.

## Project Structure
```
cosy_study_room/
    room_geometry.py    # create_floor, create_wall, create_desk, create_chair,
                        # create_bookshelf, create_bed, create_couch
    room_materials.py   # create_material, assign_material
    main.py             # ROOM_CONFIG, BUILDERS, create_element(), build_room()
    README.md           # This file
```

## Design Pattern: spec → base → details

Every builder function follows the same three-stage pattern:

- **spec** — the function parameters define what to build. No geometry exists yet.
- **base** — the first `cmds.polyCube` / `cmds.polyPlane` creates the primary structural shape.
- **details** — additional parts are built relative to the base (legs, backrest, headboard…).

All parts are collected into a list and grouped with `cmds.group()` so each prop moves as a single node.

## Data-Driven Pattern 
`ROOM_CONFIG` is a list of dicts. Each dict describes one element with keys for
`type`, `material`, dimensions, `position`, and optionally `rotation`.

## Error Handling 
`create_element()` has three layers of defence:

1. Checks `"type"` key exists — warns and skips if missing.
2. Checks the type is in `BUILDERS` — warns and skips if unknown.
3. Wraps the builder call in `try/except TypeError` — warns and skips if params are wrong.

Every geometry builder also validates its inputs before touching Maya:

- Zero or negative dimensions are replaced with the function default + `cmds.warning`.
- The full `cmds` block is wrapped in `try/except Exception`.

## Week 8 Updates

### Layout finalised from interactive scene adjustments
All furniture positions in `ROOM_CONFIG` were updated to match the final layout
produced by interactive repositioning in Maya. The cumulative transforms (move,
rotate) were recorded as MEL commands and translated back into config constants:

| Piece      | Final position (x, y, z)   | Notes                          |
|------------|----------------------------|--------------------------------|
| Desk       | (-1.0, 0, -7.22)           | Pushed to back wall            |
| Chair      | (-1.09, 0, -5.88)          | Rotated 182° to face desk      |
| Bookshelf  | (1.54, 0, -5.6)            | Along back-right wall          |
| Bed        | (-3.82, 0, -4.11)          | Back-left corner               |
| Couch      | (-4.97, 0, 0.12)           | Left wall, rotated 88°         |

### Room shell scaled to match scene
`build_room()` now groups the floor and walls separately into a node named
`"room"` and applies a uniform scale of `0.762375` — matching what was applied
interactively in Maya. Furniture remains at world scale. Both are combined under
the final `cosy_bedroom_#` group.

### Optional rotation key in ROOM_CONFIG
Config entries can now include a `"rotation": (rx, ry, rz)` key.
`create_element()` strips it from the builder params and applies it via
`cmds.xform` after the node is created, so furniture facing is data-driven.

### Materials fixed (Week 8)
- `assign_material` now uses `type="mesh"` in `listRelatives` so only actual
  polygon mesh shapes are collected 
- Bare module-level `create_material` / `assign_material` calls removed from
  `room_materials.py`; they were firing at import time before any geometry
  existed and silently failing.

## DEBUG Mode
Set `DEBUG = True` at the top of any file during development to print trace lines.
Set `DEBUG = False` before final submission to silence all `[DEBUG]` output.

## Functions

### room_geometry.py
- `create_floor(width, depth, position)` — polyPlane ground surface
- `create_wall(width, height, axis, position)` — thin polyCube wall panel; axis selects orientation
- `create_desk(width, depth, height, position)` — tabletop slab on four legs
- `create_chair(seat_width, seat_depth, seat_height, back_height, position)` — seat, backrest, four legs
- `create_bookshelf(width, height, depth, shelves, position)` — side panels, back panel, shelf boards
- `create_bed(width, length, height, position)` — frame, mattress, headboard
- `create_couch(width, depth, seat_height, back_height, position)` — seat, backrest, two armrests

### room_materials.py
- `create_material(name, color)` — Lambert shader with RGB color; returns existing shader if already created
- `assign_material(obj_name, shader_name)` — walks full mesh hierarchy and applies shader to all mesh shapes

### main.py
- `ROOM_CONFIG` — list of 8 element dicts (types: floor, wall, desk, chair, bookshelf, bed, couch)
- `BUILDERS` — dispatcher dict mapping type strings to builder functions
- `create_element(data)` — routes one config entry; handles rotation and all error cases
- `build_room()` — driver loop; creates shaders, iterates ROOM_CONFIG, applies materials, scales shell, groups result

## Material Palette

| Key        | Shader name    | RGB                  | Description         |
|------------|----------------|----------------------|---------------------|
| floor      | pale_wood      | (0.76, 0.64, 0.48)   |  light wood     |
| wall       | warm_plaster   | (0.92, 0.88, 0.82)   |  white plaster   |
| desk       | dark_wood      | (0.40, 0.26, 0.14)   |  dark wood      |
| chair      | charcoal       | (0.25, 0.25, 0.28)   |  charcoal grey  |
| bookshelf  | mid_wood       | (0.55, 0.38, 0.22)   |  warm wood    |
| bed        | soft_linen     | (0.85, 0.82, 0.76)   |  linen/cream    |
| couch      | sage_green     | (0.45, 0.55, 0.45)   |  sage green    |

## Author
Asya Hatice Cag | DIGM 131 | Drexel University