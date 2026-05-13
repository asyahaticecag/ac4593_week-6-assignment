# Cosy Bedroom Generator

## What It Does
Generates a cosy bedroom from configuration
parameters. The room contains a desk, chair, bookshelf, bed, and couch, all
placed intentionally on the floor inside two corner walls. Every piece of furniture and architecture is described as a
dictionary entry in Main, Room_geometry, Room_Materials.

## Planned Features
- Core geometry functions 
- Data-driven configuration 

## Project Structure
```
cosy_study_room/
    room_geometry.py    # create_floor, create_wall, create_desk, create_chair,
                        # create_bookshelf, create_bed, create_couch
    room_materials.py   # create_material, assign_material
    main.py             # Entry point, config constants, build_room()
    README.md           # This file
```

## Design Pattern: spec → base → details

Every builder function in this project follows the same three-stage pattern:

- **spec** — the function parameters define *what* to build (`width`, `height`, `position`, etc.). No geometry exists yet; this is just the description.
- **base** — the first `cmds.polyCube` or `cmds.polyPlane` call creates the primary structural shape (desk tabletop, bed frame, couch seat base). This alone reads as the object.
- **details** — additional parts are built relative to the base (legs, backrest, armrests, headboard, shelf boards). These give each prop its identity and silhouette.

All parts are collected into a list and grouped with `cmds.group()` so each prop moves as a single node.

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

## Author
Asya Hatice Cag | DIGM 131 | Drexel University