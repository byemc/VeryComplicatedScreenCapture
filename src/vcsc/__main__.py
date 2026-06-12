# Compilation mode, support OS-specific options
# IGNORE nuitka-project-if: {OS} in ("Windows", "Linux", "Darwin", "FreeBSD"):
# IGNORE   nuitka-project: --mode=onefile
# IGNORE nuitka-project-else:
#    nuitka-project: --mode=standalone

# Set variables dynamically and use them later, e.g., for Windows metadata
# nuitka-project-if: {OS} == "Windows":
#    nuitka-project-set: MY_VERSION = __import__("vcsc").__safe_version__
#    nuitka-project: --file-version={MY_VERSION}
#    nuitka-project: --windows-icon-from-ico={MAIN_DIRECTORY}/net.byespace.vcsc.ico
# nuitka-project: --enable-plugin=pyside6
# nuitka-project: --include-qt-plugins=multimedia
#
# nuitka-project: --include-package-data=vcsc
# nuitka-project: --windows-console-mode=disable

from vcsc import vcsc_app

vcsc_app.main()
