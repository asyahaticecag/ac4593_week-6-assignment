# Cosy Bedroom Generator

## What It Does
Generates a cosy bedroom from configuration
parameters. The room contains a desk, chair, bookshelf, bed, and couch, all
placed intentionally on the floor inside two corner walls.Every piece of furniture and architecture is described as a dictionary entry in ROOM_CONFIG inside main.py.


## Project Structure
cosy_study_room/
    room_geometry.py    # create_floor, create_wall, create_desk, create_chair,
                        # create_bookshelf, create_bed, create_couch
    room_materials.py   # create_material, assign_material
    main.py             # ROOM_CONFIG, BUILDERS, create_element(), build_room()
    README.md           # This file

## Design Pattern: spec → base → details

Every builder function in this project follows the same three-stage pattern:

spec — the function parameters define what to build. No geometry exists yet.
base — the first cmds.polyCube / cmds.polyPlane creates the primary structural shape.
details — additional parts are built relative to the base (legs, backrest, headboard…).

All parts are collected into a list and grouped with cmds.group() so each prop moves as a single node.

Data-Driven Pattern (Week 7)
ROOM_CONFIG is a list of dicts.

# Error Handling (Week 7)
create_element() has three layers of defence:

Checks "type" key exists — warns and skips if missing.
Checks the type is in BUILDERS — warns and skips if unknown.
Wraps the builder call in try/except TypeError — warns and skips if params are wrong.

Every geometry builder also validates its inputs before touching Maya:

Zero or negative dimensions are replaced with the function default + cmds.warning.
The full cmds block is wrapped in try/except Exception.

# DEBUG Mode
Set DEBUG = True at the top of any file during development to print trace lines.
Set DEBUG = False before final submission to silence all [DEBUG] output.

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
- `create_material(name, color)` — Lambert shader with RGB color
- `assign_material(obj_name, shader_name)` — Apply shader to object or group

# main.py

ROOM_CONFIG — list of 8 element dicts (5 types: floor, wall, desk, chair, bookshelf, bed, couch)
BUILDERS — dispatcher dict mapping type strings to builder functions
create_element(data) — routes one config entry; handles all error cases
build_room() — driver loop; iterates ROOM_CONFIG, applies materials, groups result

## Author
Asya Hatice Cag | DIGM 131 | Drexel University