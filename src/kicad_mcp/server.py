"""KiCad MCP Server — file-based tools for .kicad_sch and .kicad_pcb files."""

import json
from mcp.server.fastmcp import FastMCP

from kicad_mcp.tools import schematic as sch_file, pcb as pcb_file

mcp = FastMCP("kicad-file")


# ── Schematic File Tools ─────────────────────────────────────────────────────

@mcp.tool()
def get_schematic_info(filepath: str) -> str:
    """Get overview of a .kicad_sch schematic file (counts, metadata).

    Args:
        filepath: Full path to the .kicad_sch file
    """
    return json.dumps(sch_file.get_schematic_info(filepath), indent=2)


@mcp.tool()
def get_schematic_symbols(filepath: str) -> str:
    """Get all symbols in a schematic file with their properties, positions, pins.

    Args:
        filepath: Full path to the .kicad_sch file
    """
    return json.dumps(sch_file.get_schematic_symbols(filepath), indent=2)


@mcp.tool()
def get_schematic_labels(filepath: str) -> str:
    """Get all labels (local, global, hierarchical) in a schematic file.

    Args:
        filepath: Full path to the .kicad_sch file
    """
    return json.dumps(sch_file.get_schematic_labels(filepath), indent=2)


@mcp.tool()
def get_schematic_sheets(filepath: str) -> str:
    """Get hierarchical sheet references in a schematic file.

    Args:
        filepath: Full path to the .kicad_sch file
    """
    return json.dumps(sch_file.get_schematic_sheets(filepath), indent=2)


@mcp.tool()
def get_schematic_wires(filepath: str) -> str:
    """Get all wires and buses in a schematic file.

    Args:
        filepath: Full path to the .kicad_sch file
    """
    return json.dumps(sch_file.get_schematic_wires(filepath), indent=2)


@mcp.tool()
def get_schematic_lib_symbols(filepath: str) -> str:
    """Get library symbols embedded in a schematic file.

    Args:
        filepath: Full path to the .kicad_sch file
    """
    return json.dumps(sch_file.get_schematic_lib_symbols(filepath), indent=2)


# ── PCB File Tools ───────────────────────────────────────────────────────────

@mcp.tool()
def get_pcb_info(filepath: str) -> str:
    """Get overview of a .kicad_pcb file (counts, layers, metadata).

    Args:
        filepath: Full path to the .kicad_pcb file
    """
    return json.dumps(pcb_file.get_pcb_info(filepath), indent=2)


@mcp.tool()
def get_pcb_footprints(filepath: str) -> str:
    """Get all footprints in a PCB file with reference, value, position.

    Args:
        filepath: Full path to the .kicad_pcb file
    """
    return json.dumps(pcb_file.get_pcb_footprints(filepath), indent=2)


@mcp.tool()
def get_pcb_nets(filepath: str) -> str:
    """Get all nets in a PCB file.

    Args:
        filepath: Full path to the .kicad_pcb file
    """
    return json.dumps(pcb_file.get_pcb_nets(filepath), indent=2)


@mcp.tool()
def get_pcb_tracks(filepath: str) -> str:
    """Get all tracks (segments, vias, arcs) in a PCB file.

    Args:
        filepath: Full path to the .kicad_pcb file
    """
    return json.dumps(pcb_file.get_pcb_tracks(filepath), indent=2)


@mcp.tool()
def get_pcb_zones(filepath: str) -> str:
    """Get all copper zones in a PCB file.

    Args:
        filepath: Full path to the .kicad_pcb file
    """
    return json.dumps(pcb_file.get_pcb_zones(filepath), indent=2)


@mcp.tool()
def get_pcb_layers(filepath: str) -> str:
    """Get board layer definitions from a PCB file.

    Args:
        filepath: Full path to the .kicad_pcb file
    """
    return json.dumps(pcb_file.get_pcb_layers(filepath), indent=2)


@mcp.tool()
def get_pcb_setup(filepath: str) -> str:
    """Get board setup (stackup, design rules) from a PCB file.

    Args:
        filepath: Full path to the .kicad_pcb file
    """
    return json.dumps(pcb_file.get_pcb_setup(filepath), indent=2)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
