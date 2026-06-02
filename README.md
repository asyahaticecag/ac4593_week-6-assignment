# Cosy Bedroom Generator

## Overview

The Cosy Bedroom Generator is a modular Maya Python tool that procedurally builds a furnished bedroom scene from a data-driven configuration. The project demonstrates geometry generation, material assignment, error handling, modular programming, and scene assembly using Maya commands.

The room contains a floor, walls, desk, chair, bookshelf, bed, and couch. Each scene element is defined by a configuration dictionary, allowing the entire room layout to be controlled through editable data.

---

## Features

* Data-driven room generation using configuration dictionaries
* Modular project structure with separate geometry and material modules
* Automatic material creation and assignment
* Defensive error handling and input validation
* Configurable furniture dimensions and placement
* Reusable builder functions with sensible defaults
* Debug mode for development and troubleshooting

---

## Project Structure

```text
cosy_bedroom_generator/

---

main.py
     Driver script, configuration data,
     dispatcher, and room assembly logic

room_geometry.py
     Geometry builder functions for all
     architectural and furniture elements

room_materials.py
     Material creation and assignment utilities

 README.md
    Project documentation

---

## Design Pattern: Specification → Base → Details

Each geometry builder follows the same three-stage construction workflow:

### 1. Specification

Function parameters define the dimensions and placement requirements of the object.

Example:

```python
create_desk(
    width=3.5,
    depth=1.5,
    height=1.5,
    position=(-3.85, 0, -4.85)
)
```

No geometry exists during this stage.

### 2. Base

The primary structural component is created using a Maya primitive.

Examples:

* Floor → polyPlane
* Wall → polyCube

### 3. Details

Additional components are created relative to the base structure.

Examples:

* Desk legs
* Chair backrest
* Bookshelf shelves
* Bed mattress and headboard
* Couch armrests

All parts are collected into a list and grouped so the furniture behaves as a single transform node.

---

## Data-Driven Architecture

The scene is generated from the `ROOM_CONFIG` list in `main.py`.

Each dictionary represents a room element and contains information such as:

* Type
* Material
* Dimensions
* Position

---

### Dispatcher Validation

`create_element()` performs three levels of validation:

1. Verifies the configuration contains a `"type"` key.
2. Verifies the type exists in the `BUILDERS` dictionary.
3. Wraps builder execution in `try/except` blocks to catch invalid arguments or runtime errors.

### Geometry Validation

Every geometry builder validates critical dimensions before creating Maya geometry.

If invalid values are supplied:

* A warning is issued.
* A safe default value is substituted.
* Scene generation continues without crashing.

### Material Validation

Material assignment verifies:

* The object exists.
* The shader exists.
* Valid mesh shapes are found.

Warnings are generated when any requirement is missing.

---

## Debug Mode

Each module contains a DEBUG flag.

```python
DEBUG = True
```

When enabled, diagnostic information is printed to the Script Editor.

```python
DEBUG = False
```

Disables all debug output for final submission.

---

## Main Components

### room_geometry.py

Contains all geometry builder functions:

* `create_floor()`
* `create_wall()`
* `create_desk()`
* `create_chair()`
* `create_bookshelf()`
* `create_bed()`
* `create_couch()`

Each function returns the Maya transform node of the generated object.

### room_materials.py

Contains material utilities:

#### create_material()

Creates a Lambert shader with a specified RGB color.

#### assign_material()

Assigns a shader to all mesh shapes contained within an object hierarchy.

### main.py

Contains the project controller:

#### ROOM_CONFIG

Stores all room specifications.

#### BUILDERS

Maps type names to geometry builder functions.

#### create_element()

Routes configuration entries to the correct builder function.

#### build_room()

Creates materials, generates geometry, applies shaders, and assembles the final bedroom scene.

---

## Material Palette

| Material Key | Shader Name  | RGB Color          |
| ------------ | ------------ | ------------------ |
| floor        | pale_wood    | (0.76, 0.64, 0.48) |
| wall         | warm_plaster | (0.92, 0.88, 0.82) |
| desk         | dark_wood    | (0.40, 0.26, 0.14) |
| chair        | charcoal     | (0.25, 0.25, 0.28) |
| bookshelf    | mid_wood     | (0.55, 0.38, 0.22) |
| bed          | soft_linen   | (0.85, 0.82, 0.76) |
| couch        | sage_green   | (0.45, 0.55, 0.45) |

---

## Learning Objectives Demonstrated

This project demonstrates:

* Procedural modeling with Maya Python
* Modular software design
* Data-driven scene generation
* Python dictionaries and dispatch tables
* Error handling and validation
* Material creation and assignment
* Code documentation and maintainability

---

## Author

**Asya Hatice Cag**
DIGM 131 – Intro to Scripting for the DCC Pipeline
Drexel University
