
import platform

from PySide6 import QtGui


def get_platform_icon_font() -> str | None:
    system = platform.system()
    release = platform.release()
    version = platform.version()

    if system == "Windows":
        return "Segoe MDL2 Assets"

    return None

def icon(name: str) -> str:
    """Maps freedesktop icons to applicable icons on Windows and macOS."""
    if platform.system() == 'Windows':
        # The if-else of hell
        if name == "configure":
            return "\uF8B0"
        if name == "camera-photo":
            return "\uE722"
        if name == "favorite":
            return "\uE734"
        if name == "audio-input-microphone":
            return "\uE720"
        return "\uE783"
    return name

def get_icon(name: str) -> QtGui.QIcon:
    # Attempt to get it from the icon theme
    icon_from_theme = QtGui.QIcon.fromTheme(name)
    if not icon_from_theme.isNull():
        return icon_from_theme

    # Freedesktop icons not supported or this one doesn't exist.
    # Lets try from /icons
    icon_from_file = QtGui.QIcon(f"icons/22/{name}.svg")
    if not icon_from_file.isNull():
        return icon_from_file

    # Check if any transformations are available into one compatible with this OS maybe...?
    # icon_transgendered = QtGui.QIcon.fromTheme(icon(name))
    # if not icon_transgendered.
    # return icon_transgendered

    # Shit.
    return QtGui.QIcon()
