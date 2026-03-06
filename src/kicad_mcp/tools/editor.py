"""Tools for opening KiCad files in the schematic/PCB editors."""

import os
import subprocess
import sys


def _find_kicad_bin() -> str:
    """Find the KiCad bin directory."""
    if sys.platform == "win32":
        for version in ["10.0", "9.0", "8.0"]:
            path = rf"C:\Program Files\KiCad\{version}\bin"
            if os.path.isdir(path):
                return path
    else:
        # Linux/macOS: assume kicad binaries are in PATH
        return ""
    raise FileNotFoundError("KiCad installation not found")


def _exe(name: str) -> str:
    """Get full path to a KiCad executable."""
    bin_dir = _find_kicad_bin()
    if bin_dir:
        ext = ".exe" if sys.platform == "win32" else ""
        return os.path.join(bin_dir, name + ext)
    return name  # rely on PATH


def open_schematic(filepath: str) -> dict:
    """Open a .kicad_sch file in the schematic editor (eeschema)."""
    filepath = os.path.abspath(filepath)
    if not os.path.isfile(filepath):
        return {"error": f"File not found: {filepath}"}
    exe = _exe("eeschema")
    subprocess.Popen([exe, filepath], creationflags=subprocess.DETACHED_PROCESS if sys.platform == "win32" else 0)
    return {"status": "opened", "editor": "eeschema", "filepath": filepath}


def open_pcb(filepath: str) -> dict:
    """Open a .kicad_pcb file in the PCB editor (pcbnew)."""
    filepath = os.path.abspath(filepath)
    if not os.path.isfile(filepath):
        return {"error": f"File not found: {filepath}"}
    exe = _exe("pcbnew")
    subprocess.Popen([exe, filepath], creationflags=subprocess.DETACHED_PROCESS if sys.platform == "win32" else 0)
    return {"status": "opened", "editor": "pcbnew", "filepath": filepath}


def open_in_kicad(filepath: str) -> dict:
    """Open any KiCad file (.kicad_pro, .kicad_sch, .kicad_pcb) in the appropriate editor."""
    filepath = os.path.abspath(filepath)
    if not os.path.isfile(filepath):
        return {"error": f"File not found: {filepath}"}

    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".kicad_sch":
        return open_schematic(filepath)
    elif ext == ".kicad_pcb":
        return open_pcb(filepath)
    elif ext == ".kicad_pro":
        exe = _exe("kicad")
        subprocess.Popen([exe, filepath], creationflags=subprocess.DETACHED_PROCESS if sys.platform == "win32" else 0)
        return {"status": "opened", "editor": "kicad", "filepath": filepath}
    else:
        return {"error": f"Unsupported file extension: {ext}"}
