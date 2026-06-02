# Cosy Bedroom Generator

## What It Does

Generates a cosy bedroom scene from configuration parameters. The room contains a floor, walls, desk, chair, bookshelves, bed, and couch. Every piece of furniture and architecture is described as a dictionary entry in `ROOM_CONFIG` inside `main.py`.

The project uses a data-driven system: each dictionary entry stores the object type, material, dimensions, position, and optional rotation. The driver loop reads this data, sends it to the correct builder function, applies materials, and groups the completed room into one final scene.

## Project Structure

cosy_bedroom_generator/

    main.py
        ROOM_CONFIG
        MATERIAL_PALETTE
        BUILDERS
        create_element()
        build_room()

    room_geometry.py
        create_floor()
        create_wall()
        create_desk()
        create_chair()
        create_bookshelf()
        create_bed()
        create_couch()

    room_materials.py
        create_material()
        assign_material()

    room_io.py
        save_config()
        load_config()

    room_ui.py
        build_ui()
        on_build_clicked()
        on_save_clicked()
        on_load_clicked()

    README.md
        Project documentation


## Design Pattern: spec → base → details

Every builder function follows the same three-stage pattern:

* **spec** — the function parameters define what to build. No geometry exists yet.
* **base** — the first `cmds.polyCube` or `cmds.polyPlane` creates the primary structural shape.
* **details** — additional parts are built relative to the base, such as legs, backrests, shelves, mattresses, and armrests.

All parts are collected into a list and grouped with `cmds.group()` so each piece of furniture moves as a single node.

## Data-Driven Pattern

`ROOM_CONFIG` is a list of dictionaries. Each dictionary describes one scene element with keys for:

* `type`
* `material`
* dimensions
* `position`
* optional `rotation`

Example:


{
    "type": "chair",
    "material": "chair",
    "seat_width": 0.9,
    "seat_depth": 0.9,
    "seat_height": 1.0,
    "back_height": 0.8,
    "position": (0.2, 0, -3.0),
    "rotation": (0, 180, 0),
}


The driver loop does not manually call each furniture function. Instead, it reads the `"type"` key, finds the matching function inside `BUILDERS`, and passes the remaining data into that builder.

## Error Handling

`create_element()` has three layers of defence:

1. Checks that the config entry is a dictionary.
2. Checks that the `"type"` key exists.
3. Checks that the type exists inside `BUILDERS`.
4. Wraps the builder call in `try/except` so bad parameters do not crash the full room build.

Every geometry builder also validates inputs before touching Maya:

* Zero or negative dimensions are replaced with safe defaults.
* `cmds.warning()` gives feedback when invalid values are found.
* Maya command blocks are wrapped in `try/except Exception`.

## Material Assignment

Materials are created in `room_materials.py` using Lambert shaders.

The `assign_material()` function is designed to work with both single objects and grouped furniture. For example, `chair_1` is a group, but its actual mesh pieces are named things like:

* `seat_1`
* `backrest_1`
* `chair_leg_1`
* `chair_leg_2`
* `chair_leg_3`
* `chair_leg_4`

The material assignment function searches through the full hierarchy, finds all mesh shapes under the group, and assigns the shader to those mesh shapes instead of assigning only to the group transform.

## Week 9 Updates

### JSON Save and Load

A new file, `room_io.py`, adds JSON support.

* `save_config(config)` saves `ROOM_CONFIG` to a JSON file.
* `load_config()` loads the saved JSON file and returns the room data.

This allows the room configuration to persist outside Maya.

### Maya UI

A new file, `room_ui.py`, adds a simple Maya tool window.

The UI includes:

* **Build Room** button
* **Save Config JSON** button
* **Load Config JSON** button

The UI does not directly create geometry. It calls functions from `main.py` and `room_io.py`, keeping the interface separate from the scene-building logic.

### Rotation Support

The project now supports an optional `"rotation"` key in `ROOM_CONFIG`.

This allows selected furniture, such as the chair and couch, to be rotated directly from the configuration data instead of manually rotating them after creation.

## DEBUG Mode

Set `DEBUG = True` at the top of a file during development to print trace lines.

```python
DEBUG = True
```

Set `DEBUG = False` before final submission to silence debug output.

```python
DEBUG = False
```

## Functions

### room_geometry.py

* `create_floor(width, depth, position)` — creates a flat polyPlane floor.
* `create_wall(width, height, axis, position)` — creates a thin wall panel along the X or Z axis.
* `create_desk(width, depth, height, position)` — creates a tabletop and four legs.
* `create_chair(seat_width, seat_depth, seat_height, back_height, position)` — creates a chair with seat, backrest, and four legs.
* `create_bookshelf(width, height, depth, shelves, position)` — creates side panels, back panel, and shelf boards.
* `create_bed(width, length, height, position)` — creates bed frame, mattress, and headboard.
* `create_couch(width, depth, seat_height, back_height, position)` — creates base, seat, backrest, and armrests.

### room_materials.py

* `create_material(name, color)` — creates a Lambert shader with RGB color values.
* `assign_material(obj_name, shader_name)` — finds all mesh shapes under an object or group and assigns the selected shader.

### room_io.py

* `save_config(config)` — saves the room configuration to JSON.
* `load_config()` — loads the saved room configuration from JSON.

### room_ui.py

* `build_ui()` — creates the Maya tool window.
* `on_build_clicked()` — calls `main.build_room()`.
* `on_save_clicked()` — saves `ROOM_CONFIG` to JSON.
* `on_load_clicked()` — loads JSON data and rebuilds the room.

### main.py

* `ROOM_CONFIG` — list of dictionaries describing every room element.
* `MATERIAL_PALETTE` — material names and RGB colors.
* `BUILDERS` — dispatcher dictionary mapping type strings to builder functions.
* `create_element(data)` — validates one config entry, dispatches it, and applies optional rotation.
* `build_room()` — creates materials, builds all room elements, applies shaders, and groups the final scene.

## Material Palette

| Key       | Shader name  | RGB                | Description        |
| --------- | ------------ | ------------------ | ------------------ |
| floor     | pale_wood    | (0.76, 0.64, 0.48) | light wooden floor |
| wall      | warm_plaster | (0.92, 0.88, 0.82) | warm plaster wall  |
| desk      | dark_wood    | (0.40, 0.26, 0.14) | dark wooden desk   |
| chair     | mid_wood     | (0.55, 0.38, 0.22) | wooden chair       |
| bookshelf | mid_wood     | (0.55, 0.38, 0.22) | wooden shelves     |
| bed       | soft_linen   | (0.85, 0.82, 0.76) | soft linen bed     |
| couch     | sage_green   | (0.45, 0.55, 0.45) | sage green couch   |

## How to Run

Open Maya and run the UI file:

import room_ui
room_ui.build_ui()

Then use the buttons in the tool window to build the room, save the configuration, or load a saved configuration.

## Author

Asya Hatice Cag | DIGM 131 | Drexel University
