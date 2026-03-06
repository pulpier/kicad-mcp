"""KiCad MCP Server — file-based tools for .kicad_sch and .kicad_pcb files."""

import json
from mcp.server.fastmcp import FastMCP

from kicad_mcp.tools import schematic as sch_file, pcb as pcb_file, editor, symbol_edit, wire_edit

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


# ── Symbol Edit Tools ───────────────────────────────────────────────────────

@mcp.tool()
def move_symbol(filepath: str, reference: str = None, uuid: str = None,
                x: float = None, y: float = None, angle: float = None) -> str:
    """Move a symbol to a new position in a schematic.

    Identify the symbol by reference (e.g. "R1") or UUID.
    Only provided coordinates are changed; others stay the same.

    Args:
        filepath: Full path to the .kicad_sch file
        reference: Reference designator (e.g. "R1", "C3")
        uuid: Symbol UUID (alternative to reference)
        x: New X position (mm)
        y: New Y position (mm)
        angle: New rotation angle (degrees)
    """
    return json.dumps(symbol_edit.move_symbol(filepath, reference, uuid, x, y, angle), indent=2)


@mcp.tool()
def set_symbol_property(filepath: str, key: str, value: str,
                        reference: str = None, uuid: str = None) -> str:
    """Set a property on a symbol (e.g. Reference, Value, Footprint).

    If the property doesn't exist, it is added.

    Args:
        filepath: Full path to the .kicad_sch file
        key: Property name (e.g. "Value", "Footprint", "Reference")
        value: New property value
        reference: Reference designator to identify the symbol
        uuid: Symbol UUID (alternative to reference)
    """
    return json.dumps(symbol_edit.set_symbol_property(filepath, key, value, reference, uuid), indent=2)


@mcp.tool()
def set_symbol_properties(filepath: str, properties: dict,
                          reference: str = None, uuid: str = None) -> str:
    """Set multiple properties on a symbol at once.

    Args:
        filepath: Full path to the .kicad_sch file
        properties: Dict of key-value pairs, e.g. {"Value": "10k", "Footprint": "R_0603"}
        reference: Reference designator to identify the symbol
        uuid: Symbol UUID (alternative to reference)
    """
    return json.dumps(symbol_edit.set_symbol_properties(filepath, properties, reference, uuid), indent=2)


@mcp.tool()
def delete_symbol(filepath: str, reference: str = None, uuid: str = None) -> str:
    """Delete a symbol from the schematic.

    Warning: does NOT remove connected wires or labels.

    Args:
        filepath: Full path to the .kicad_sch file
        reference: Reference designator to identify the symbol
        uuid: Symbol UUID (alternative to reference)
    """
    return json.dumps(symbol_edit.delete_symbol(filepath, reference, uuid), indent=2)


@mcp.tool()
def duplicate_symbol(filepath: str, new_reference: str,
                     x: float = None, y: float = None,
                     reference: str = None, uuid: str = None) -> str:
    """Duplicate a symbol with a new reference designator.

    The copy gets a new UUID. Position defaults to original offset by (10, 0).

    Args:
        filepath: Full path to the .kicad_sch file
        new_reference: Reference designator for the copy (e.g. "R2")
        x: X position for the copy
        y: Y position for the copy
        reference: Reference designator of the symbol to duplicate
        uuid: UUID of the symbol to duplicate
    """
    return json.dumps(symbol_edit.duplicate_symbol(filepath, new_reference, x, y, reference, uuid), indent=2)


@mcp.tool()
def mirror_symbol(filepath: str, axis: str = "y",
                  reference: str = None, uuid: str = None) -> str:
    """Mirror a symbol along an axis.

    Args:
        filepath: Full path to the .kicad_sch file
        axis: "x" or "y" (default "y")
        reference: Reference designator to identify the symbol
        uuid: Symbol UUID (alternative to reference)
    """
    return json.dumps(symbol_edit.mirror_symbol(filepath, axis, reference, uuid), indent=2)


@mcp.tool()
def set_symbol_dnp(filepath: str, dnp: bool,
                   reference: str = None, uuid: str = None) -> str:
    """Set or clear the Do-Not-Populate flag on a symbol.

    Args:
        filepath: Full path to the .kicad_sch file
        dnp: True to mark as DNP, False to clear
        reference: Reference designator to identify the symbol
        uuid: Symbol UUID (alternative to reference)
    """
    return json.dumps(symbol_edit.set_symbol_dnp(filepath, dnp, reference, uuid), indent=2)


# ── Wire & Label Edit Tools ─────────────────────────────────────────────────

@mcp.tool()
def add_wire(filepath: str, x1: float, y1: float, x2: float, y2: float) -> str:
    """Add a wire between two points in a schematic.

    Args:
        filepath: Full path to the .kicad_sch file
        x1: Start X (mm)
        y1: Start Y (mm)
        x2: End X (mm)
        y2: End Y (mm)
    """
    return json.dumps(wire_edit.add_wire(filepath, x1, y1, x2, y2), indent=2)


@mcp.tool()
def add_wire_path(filepath: str, points: list[dict]) -> str:
    """Add a multi-segment wire path. Each segment connects consecutive points.

    Args:
        filepath: Full path to the .kicad_sch file
        points: List of {"x": float, "y": float} dicts, minimum 2 points
    """
    return json.dumps(wire_edit.add_wire_path(filepath, points), indent=2)


@mcp.tool()
def delete_wire(filepath: str, uuid: str) -> str:
    """Delete a wire by UUID.

    Args:
        filepath: Full path to the .kicad_sch file
        uuid: UUID of the wire to delete
    """
    return json.dumps(wire_edit.delete_wire(filepath, uuid), indent=2)


@mcp.tool()
def add_junction(filepath: str, x: float, y: float) -> str:
    """Add a junction at a point where wires cross.

    Args:
        filepath: Full path to the .kicad_sch file
        x: X position (mm)
        y: Y position (mm)
    """
    return json.dumps(wire_edit.add_junction(filepath, x, y), indent=2)


@mcp.tool()
def delete_junction(filepath: str, uuid: str) -> str:
    """Delete a junction by UUID.

    Args:
        filepath: Full path to the .kicad_sch file
        uuid: UUID of the junction to delete
    """
    return json.dumps(wire_edit.delete_junction(filepath, uuid), indent=2)


@mcp.tool()
def add_label(filepath: str, text: str, x: float, y: float,
              angle: float = 0) -> str:
    """Add a local net label at a position in the schematic.

    Args:
        filepath: Full path to the .kicad_sch file
        text: Label text (net name)
        x: X position (mm)
        y: Y position (mm)
        angle: Rotation angle in degrees (default 0)
    """
    return json.dumps(wire_edit.add_label(filepath, text, x, y, angle), indent=2)


@mcp.tool()
def add_global_label(filepath: str, text: str, x: float, y: float,
                     angle: float = 0, shape: str = "input") -> str:
    """Add a global label at a position in the schematic.

    Args:
        filepath: Full path to the .kicad_sch file
        text: Label text (net name)
        x: X position (mm)
        y: Y position (mm)
        angle: Rotation angle in degrees (default 0)
        shape: One of "input", "output", "bidirectional", "tri_state", "passive"
    """
    return json.dumps(wire_edit.add_global_label(filepath, text, x, y, angle, shape), indent=2)


@mcp.tool()
def delete_label(filepath: str, uuid: str) -> str:
    """Delete a label (local or global) by UUID.

    Args:
        filepath: Full path to the .kicad_sch file
        uuid: UUID of the label to delete
    """
    return json.dumps(wire_edit.delete_label(filepath, uuid), indent=2)


@mcp.tool()
def move_label(filepath: str, uuid: str, x: float = None, y: float = None,
               angle: float = None) -> str:
    """Move a label (local or global) to a new position.

    Args:
        filepath: Full path to the .kicad_sch file
        uuid: UUID of the label to move
        x: New X position (mm)
        y: New Y position (mm)
        angle: New rotation angle (degrees)
    """
    return json.dumps(wire_edit.move_label(filepath, uuid, x, y, angle), indent=2)


# ── Editor Tools ────────────────────────────────────────────────────────────

@mcp.tool()
def open_schematic(filepath: str) -> str:
    """Open a .kicad_sch file in the KiCad schematic editor (eeschema).

    Args:
        filepath: Full path to the .kicad_sch file
    """
    return json.dumps(editor.open_schematic(filepath), indent=2)


@mcp.tool()
def open_pcb(filepath: str) -> str:
    """Open a .kicad_pcb file in the KiCad PCB editor (pcbnew).

    Args:
        filepath: Full path to the .kicad_pcb file
    """
    return json.dumps(editor.open_pcb(filepath), indent=2)


@mcp.tool()
def open_in_kicad(filepath: str) -> str:
    """Open any KiCad file (.kicad_pro, .kicad_sch, .kicad_pcb) in the appropriate editor.

    Args:
        filepath: Full path to the KiCad file
    """
    return json.dumps(editor.open_in_kicad(filepath), indent=2)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
