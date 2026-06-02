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
    """Load ROOM_CONFIG from JSON and rebuild the room."""
    config = room_io.load_config()

    if config:
        Main.ROOM_CONFIG[:] = config
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

    cmds.showWindow(WINDOW_NAME)


# ---------------------------------------------------------
# Run directly
# ---------------------------------------------------------

if __name__ == "__main__":
    build_ui()
