import json
import os
import maya.cmds as cmds


EXPORT_DIR = os.path.join(
    os.path.expanduser("~"),
    "maya_exports"
)

JSON_FILE = os.path.join(
    EXPORT_DIR,
    "cosy_bedroom.json"
)


def save_config(config):
    """
    Save ROOM_CONFIG to JSON.
    """

    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)

    with open(JSON_FILE,
              "w",
              encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    print("Saved:", JSON_FILE)


def load_config():
    """
    Load ROOM_CONFIG from JSON.
    """

    if not os.path.isfile(JSON_FILE):
        cmds.warning("JSON file not found.")
        return []

    with open(JSON_FILE,
              "r",
              encoding="utf-8") as f:
        return json.load(f)