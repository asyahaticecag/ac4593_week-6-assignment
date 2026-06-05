# Cosy Bedroom Generator

## What It Does

Generates a cosy bedroom scene from configuration parameters. The room contains a floor, walls, desk, chair, bookshelves, bed, and couch. Every piece of furniture and architectural element is described as a dictionary entry in `ROOM_CONFIG` inside `Main.py`.

The project follows a data-driven workflow. Each dictionary stores the object type, material, dimensions, and position. The driver loop reads this data, dispatches it to the correct builder function, applies materials, and assembles the completed room automatically.

---

## Project Structure


cosy_bedroom_generator/

    Main.py
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
        on_tweak_clicked()

    README.md
        Project documentation


---

## Design Pattern: spec → base → details

Every builder function follows the same three-stage pattern:

* **spec** — function parameters define what will be built.
* **base** — the first `cmds.polyCube()` or `cmds.polyPlane()` creates the primary structural shape.
* **details** — additional geometry is built relative to the base shape, such as desk legs, chair backrests, shelves, mattresses, and couch armrests.

All furniture pieces are grouped with `cmds.group()` so they can be manipulated as a single object.

---

## Data-Driven Pattern

`ROOM_CONFIG` is a list of dictionaries. Each dictionary describes one room element using keys such as:

* type
* material
* dimensions
* position

Example:

```python
{
    "type": "chair",
    "material": "chair",
    "seat_width": 0.9,
    "seat_depth": 0.9,
    "seat_height": 1.0,
    "back_height": 0.8,
    "position": (0.2, 0, -3.0),
}
```

The driver loop does not manually call geometry functions. Instead, it uses the `"type"` key to look up the correct builder inside `BUILDERS` and dispatches the configuration automatically.

---

## Error Handling

`create_element()` uses multiple layers of defensive programming:

1. Checks that the config entry is a dictionary.
2. Checks that the `"type"` key exists.
3. Checks that the type exists inside `BUILDERS`.
4. Wraps the builder call in `try/except` blocks to prevent crashes.

Geometry builders also validate user input before creating geometry:

* Invalid dimensions are replaced with safe defaults.
* `cmds.warning()` reports invalid values.
* Maya commands are wrapped in `try/except Exception`.

---

## Material Assignment

Materials are created in `room_materials.py` using Lambert shaders.

The material assignment system supports both individual mesh objects and grouped furniture.

For example:

```text
chair_1
    seat_1
    backrest_1
    chair_leg_1
    chair_leg_2
    chair_leg_3
    chair_leg_4
```

Instead of assigning materials to the transform group, the script searches through the hierarchy, finds every mesh shape, and applies the shader directly to the geometry.

---

## Week 9 Updates

### JSON Save and Load

The project includes JSON support through `room_io.py`.

Functions:

* `save_config(config)`
* `load_config()`

This allows room configuration data to be stored outside Maya and reloaded later.

---

### Maya UI

The project includes a custom Maya UI built in `room_ui.py`.

Available buttons:

* **Build Room**
* **Save Config JSON**
* **Load Config JSON**
* **Tweak Room Layout**

The UI does not create geometry directly. Instead, it calls functions from the project modules.

---

### Alternative Layout System

The **Tweak Room Layout** button creates a second room arrangement by modifying object positions before rebuilding the room.

This demonstrates how the same data-driven system can generate multiple room layouts without modifying the geometry builders.

---

### Material Assignment Improvements

Material assignment was updated to:

* Support grouped furniture.
* Search complete hierarchies.
* Assign shaders to mesh shapes rather than transform groups.

---

## DEBUG Mode

Each module contains a DEBUG flag.

## Functions

### Main.py

* `ROOM_CONFIG` — room configuration data.
* `MATERIAL_PALETTE` — shader definitions and RGB values.
* `BUILDERS` — dispatcher dictionary.
* `create_element(data)` — validates and creates one room element.
* `build_room()` — builds the complete room scene.

### room_geometry.py

* `create_floor()` — creates a floor plane.
* `create_wall()` — creates wall geometry.
* `create_desk()` — creates a desk.
* `create_chair()` — creates a chair.
* `create_bookshelf()` — creates a bookshelf.
* `create_bed()` — creates a bed.
* `create_couch()` — creates a couch.

### room_materials.py

* `create_material()` — creates Lambert shaders.
* `assign_material()` — assigns materials to mesh shapes.

### room_io.py

* `save_config()` — saves room configuration to JSON.
* `load_config()` — loads room configuration from JSON.

### room_ui.py

* `build_ui()` — creates the Maya interface.
* `on_build_clicked()` — builds the room.
* `on_save_clicked()` — saves JSON data.
* `on_load_clicked()` — loads JSON data and rebuilds.
* `on_tweak_clicked()` — builds an alternate room layout.

---

## Material Palette

| Key       | Shader Name  | RGB                | Description        |
| --------- | ------------ | ------------------ | ------------------ |
| floor     | pale_wood    | (0.76, 0.64, 0.48) | Light wooden floor |
| wall      | warm_plaster | (0.92, 0.88, 0.82) | Warm plaster wall  |
| desk      | dark_wood    | (0.40, 0.26, 0.14) | Dark wooden desk   |
| chair     | mid_wood     | (0.55, 0.38, 0.22) | Wooden chair       |
| bookshelf | mid_wood     | (0.55, 0.38, 0.22) | Wooden bookshelf   |
| bed       | soft_linen   | (0.85, 0.82, 0.76) | Soft linen bed     |
| couch     | sage_green   | (0.45, 0.55, 0.45) | Sage green couch   |

---

## How to Run

Open Maya and run:

```python
import room_ui
room_ui.build_ui()
```

Use the UI buttons to:

* Build the room
* Save JSON data
* Load JSON data
* Generate an alternate room layout

---

## Author

**Asya Hatice Cag**
DIGM 131 — Drexel University
