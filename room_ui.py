"""
room_ui.py -- Maya UI for the Cosy Bedroom Generator.
====================================================
DIGM 131 - Week 9 | Author: Asya Hatice Cag | Drexel University

Creates a simple Maya tool window for building the room, saving the
configuration to JSON, and loading a saved configuration.
"""

import os
import sys
import maya.cmds as cmds

# ---------------------------------------------------------
# Make sure Maya can find sibling files
# ---------------------------------------------------------

try:
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    THIS_DIR = cmds.workspace(query=True, rootDirectory=True)

if THIS_DIR not in sys.path:
    sys.path.insert(0, THIS_DIR)

# Project modules
import Main
import room_io

WINDOW_NAME = "cosyBedroomTool"


# ---------------------------------------------------------
# Button callbacks
# ---------------------------------------------------------

def on_build_clicked(*args):
    """Build the room from ROOM_CONFIG."""
    Main.build_room()


def on_save_clicked(*args):
    """Save ROOM_CONFIG to JSON."""
    room_io.save_config(Main.ROOM_CONFIG)


def on_load_clicked(*args):
    """Load JSON and rebuild the room."""

    config = room_io.load_config()

    if not config:
        cmds.warning("No JSON data was loaded.")
        return

    Main.ROOM_CONFIG = config

    print(
        "Loaded JSON config with {} entries.".format(
            len(Main.ROOM_CONFIG)
        )
    )

    Main.build_room()


def on_tweak_clicked(*args):
    """Apply an alternate room layout and rebuild."""

    bookshelf_count = 0

    for item in Main.ROOM_CONFIG:

        if item["type"] == "bed":
            item["position"] = (-4.7, 0, 4.0)

        elif item["type"] == "desk":
            item["position"] = (-1.5, 0, 5.0)

        elif item["type"] == "bookshelf":
            bookshelf_count += 1

            if bookshelf_count == 1:
                item["position"] = (-3.5, 0, -5.6)

            elif bookshelf_count == 2:
                item["position"] = (-4.9, 0, -5.6)

    Main.build_room()

# ---------------------------------------------------------
# UI Builder
# ---------------------------------------------------------

def build_ui():
    """Create and display the Maya UI window."""

    if cmds.window(WINDOW_NAME, exists=True):
        cmds.deleteUI(WINDOW_NAME)

    cmds.window(
        WINDOW_NAME,
        title="Cosy Bedroom Generator",
        widthHeight=(350, 180)
    )

    cmds.columnLayout(
        adjustableColumn=True
    )

    cmds.text(
        label="Cosy Bedroom Generator"
    )

    cmds.separator(height=10)

    cmds.button(
        label="Build Room",
        command=on_build_clicked
    )

    cmds.button(
        label="Save Config JSON",
        command=on_save_clicked
    )

    cmds.button(
        label="Load Config JSON",
        command=on_load_clicked
    )

    cmds.separator(height=10)

    cmds.button(
        label="Tweak Room Layout",
        command=on_tweak_clicked
    )

    cmds.showWindow(WINDOW_NAME)


# ---------------------------------------------------------
# Run directly
# ---------------------------------------------------------

if __name__ == "__main__":
    build_ui()
