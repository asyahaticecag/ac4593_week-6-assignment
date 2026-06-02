import maya.cmds as cmds
import main
import room_io


WINDOW_NAME = "cosyBedroomTool"


def on_build_clicked(*args):
    main.build_room()


def on_save_clicked(*args):
    room_io.save_config(main.ROOM_CONFIG)


def on_load_clicked(*args):
    config = room_io.load_config()

    if config:
        main.ROOM_CONFIG[:] = config
        main.build_room()


def build_ui():

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

    if __name__ == "__main__":
        build_ui()  