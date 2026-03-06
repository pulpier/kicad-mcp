"""KiCad MCP Server — exposes KiCad IPC API and file parsing tools."""

import json
import traceback
from mcp.server.fastmcp import FastMCP

from kicad_mcp.tools import base, document, items, selection, board, project, utility
from kicad_mcp.tools import schematic as sch_file, pcb as pcb_file

mcp = FastMCP("kicad")


# ── Base ──────────────────────────────────────────────────────────────────────

@mcp.tool()
def ping() -> str:
    """Check if KiCad is running and responsive."""
    return base.ping()


@mcp.tool()
def get_version() -> str:
    """Get KiCad version and API version."""
    return json.dumps(base.get_version(), indent=2)


@mcp.tool()
def get_open_documents(document_type: str | None = None) -> str:
    """List open documents in KiCad.

    Args:
        document_type: Filter by type: "schematic" or "pcb". None returns all.
    """
    return json.dumps(base.get_open_documents(document_type), indent=2)


# ── Document ──────────────────────────────────────────────────────────────────

@mcp.tool()
def save_document(document_type: str, filename: str) -> str:
    """Save an open document.

    Args:
        document_type: "schematic" or "pcb"
        filename: Document filename (e.g. "myboard.kicad_pcb")
    """
    return document.save_document(document_type, filename)


@mcp.tool()
def save_document_copy(document_type: str, filename: str, new_path: str) -> str:
    """Save a copy of an open document to a new path.

    Args:
        document_type: "schematic" or "pcb"
        filename: Current document filename
        new_path: Full path for the copy
    """
    return document.save_document_copy(document_type, filename, new_path)


@mcp.tool()
def revert_document(document_type: str, filename: str) -> str:
    """Revert a document to its last saved state.

    Args:
        document_type: "schematic" or "pcb"
        filename: Document filename
    """
    return document.revert_document(document_type, filename)


@mcp.tool()
def get_document_as_string(document_type: str, filename: str) -> str:
    """Get the full document content as a KiCad s-expression string.

    Args:
        document_type: "schematic" or "pcb"
        filename: Document filename
    """
    return document.get_document_as_string(document_type, filename)


@mcp.tool()
def get_title_block_info(document_type: str, filename: str) -> str:
    """Get title block info (title, date, revision, company, comments).

    Args:
        document_type: "schematic" or "pcb"
        filename: Document filename
    """
    return json.dumps(document.get_title_block_info(document_type, filename), indent=2)


# ── Items ─────────────────────────────────────────────────────────────────────

@mcp.tool()
def get_items(document_type: str, filename: str, item_types: list[str]) -> str:
    """Get items from a schematic or PCB document by type.

    Args:
        document_type: "schematic" or "pcb"
        filename: Document filename
        item_types: List of item type names. PCB types: pcb_footprint, pcb_pad,
            pcb_track, pcb_via, pcb_zone, pcb_text, pcb_shape, pcb_arc,
            pcb_dimension, pcb_group. Schematic types: sch_symbol, sch_line,
            sch_label, sch_global_label, sch_hier_label, sch_junction,
            sch_no_connect, sch_sheet, sch_pin, sch_text, sch_textbox,
            sch_shape, sch_field, sch_directive_label, sch_bus_wire_entry,
            sch_bus_bus_entry, sch_bitmap, sch_table, sch_sheet_pin, sch_marker.
    """
    return json.dumps(items.get_items(document_type, filename, item_types), indent=2)


@mcp.tool()
def create_items(document_type: str, filename: str, items_kicad_string: str) -> str:
    """Create items from KiCad s-expression format string.

    The string should contain valid KiCad s-expressions for the item types
    (e.g. footprint definitions, track segments, symbols, wires, etc.).

    Args:
        document_type: "schematic" or "pcb"
        filename: Document filename
        items_kicad_string: KiCad s-expression string with items to create
    """
    result = items.create_items(document_type, filename, items_kicad_string)
    return json.dumps(result, indent=2)


@mcp.tool()
def delete_items(document_type: str, filename: str, item_ids: list[str]) -> str:
    """Delete items by their KiCad UUIDs.

    Args:
        document_type: "schematic" or "pcb"
        filename: Document filename
        item_ids: List of item UUID strings
    """
    result = items.delete_items(document_type, filename, item_ids)
    return json.dumps(result, indent=2)


# ── Selection ─────────────────────────────────────────────────────────────────

@mcp.tool()
def get_selection() -> str:
    """Get the currently selected items in the active editor."""
    return json.dumps(selection.get_selection(), indent=2)


@mcp.tool()
def get_selection_as_string() -> str:
    """Get the current selection as a KiCad s-expression string."""
    return selection.get_selection_as_string()


@mcp.tool()
def add_to_selection(item_ids: list[str]) -> str:
    """Add items to the current selection by UUID.

    Args:
        item_ids: List of item UUID strings
    """
    return selection.add_to_selection(item_ids)


@mcp.tool()
def remove_from_selection(item_ids: list[str]) -> str:
    """Remove items from the current selection by UUID.

    Args:
        item_ids: List of item UUID strings
    """
    return selection.remove_from_selection(item_ids)


@mcp.tool()
def clear_selection() -> str:
    """Clear the current selection in the active editor."""
    return selection.clear_selection()


@mcp.tool()
def hit_test(x_mm: float, y_mm: float, tolerance_mm: float = 0.0) -> str:
    """Find items at a given position (hit test).

    Args:
        x_mm: X coordinate in millimeters
        y_mm: Y coordinate in millimeters
        tolerance_mm: Hit test tolerance in millimeters
    """
    return json.dumps(selection.hit_test(x_mm, y_mm, tolerance_mm), indent=2)


# ── Board ─────────────────────────────────────────────────────────────────────

@mcp.tool()
def get_board_stackup(filename: str) -> str:
    """Get the PCB layer stackup configuration.

    Args:
        filename: PCB filename (e.g. "myboard.kicad_pcb")
    """
    return json.dumps(board.get_board_stackup(filename), indent=2)


@mcp.tool()
def get_nets(filename: str) -> str:
    """Get all nets in the PCB.

    Args:
        filename: PCB filename
    """
    return json.dumps(board.get_nets(filename), indent=2)


@mcp.tool()
def get_net_class_for_nets(net_names: list[str]) -> str:
    """Get net class assignments for specific nets.

    Args:
        net_names: List of net names to query
    """
    return json.dumps(board.get_net_class_for_nets(net_names), indent=2)


@mcp.tool()
def get_board_origin(filename: str) -> str:
    """Get the board origin coordinates.

    Args:
        filename: PCB filename
    """
    return json.dumps(board.get_board_origin(filename), indent=2)


@mcp.tool()
def set_board_origin(filename: str, x_mm: float, y_mm: float) -> str:
    """Set the board origin coordinates.

    Args:
        filename: PCB filename
        x_mm: X coordinate in millimeters
        y_mm: Y coordinate in millimeters
    """
    return board.set_board_origin(filename, x_mm, y_mm)


@mcp.tool()
def get_enabled_layers(filename: str) -> str:
    """Get the list of enabled board layers.

    Args:
        filename: PCB filename
    """
    return json.dumps(board.get_enabled_layers(filename), indent=2)


@mcp.tool()
def get_active_layer(filename: str) -> str:
    """Get the currently active board layer.

    Args:
        filename: PCB filename
    """
    return json.dumps(board.get_active_layer(filename), indent=2)


@mcp.tool()
def set_active_layer(filename: str, layer: int) -> str:
    """Set the active board layer.

    Args:
        filename: PCB filename
        layer: Layer number to activate
    """
    return board.set_active_layer(filename, layer)


@mcp.tool()
def refill_zones(filename: str) -> str:
    """Refill all copper zones in the PCB.

    Args:
        filename: PCB filename
    """
    return board.refill_zones(filename)


@mcp.tool()
def get_board_appearance() -> str:
    """Get the PCB editor appearance settings."""
    return json.dumps(board.get_board_appearance(), indent=2)


# ── Project ───────────────────────────────────────────────────────────────────

@mcp.tool()
def get_net_classes() -> str:
    """Get project net class definitions."""
    return json.dumps(project.get_net_classes(), indent=2)


@mcp.tool()
def get_text_variables() -> str:
    """Get project text variables."""
    return json.dumps(project.get_text_variables(), indent=2)


@mcp.tool()
def set_text_variables(variables: dict) -> str:
    """Set project text variables.

    Args:
        variables: Dictionary of variable name to value mappings
    """
    return project.set_text_variables(variables)


@mcp.tool()
def expand_text_variables(document_type: str, filename: str, text: str) -> str:
    """Expand text variables in a string (e.g. "${REVISION}" -> "1.0").

    Args:
        document_type: "schematic" or "pcb"
        filename: Document filename
        text: Text containing ${VARIABLE} references
    """
    return project.expand_text_variables(document_type, filename, text)


# ── Utility ───────────────────────────────────────────────────────────────────

@mcp.tool()
def get_text_extents(text: str, font_size_mm: float = 1.27,
                     bold: bool = False, italic: bool = False) -> str:
    """Get the bounding box of rendered text.

    Args:
        text: The text to measure
        font_size_mm: Font size in millimeters (default 1.27)
        bold: Whether text is bold
        italic: Whether text is italic
    """
    return json.dumps(utility.get_text_extents(text, font_size_mm, bold, italic), indent=2)


@mcp.tool()
def get_text_as_shapes(text: str, font_size_mm: float = 1.27,
                       bold: bool = False, italic: bool = False) -> str:
    """Convert text to geometric shapes (polygons/lines).

    Args:
        text: The text to convert
        font_size_mm: Font size in millimeters (default 1.27)
        bold: Whether text is bold
        italic: Whether text is italic
    """
    return json.dumps(utility.get_text_as_shapes(text, font_size_mm, bold, italic), indent=2)


@mcp.tool()
def run_action(action: str) -> str:
    """Run a KiCad tool action by name.

    WARNING: Action names are not stable across versions.

    Args:
        action: The KiCad TOOL_ACTION name
    """
    return json.dumps(utility.run_action(action), indent=2)


# ── Schematic File Tools (kiutils) ────────────────────────────────────────────

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


# ── PCB File Tools (kiutils) ─────────────────────────────────────────────────

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
def get_pcb_nets_from_file(filepath: str) -> str:
    """Get all nets in a PCB file.

    Args:
        filepath: Full path to the .kicad_pcb file
    """
    return json.dumps(pcb_file.get_pcb_nets(filepath), indent=2)


@mcp.tool()
def get_pcb_tracks_from_file(filepath: str) -> str:
    """Get all tracks (segments, vias, arcs) in a PCB file.

    Args:
        filepath: Full path to the .kicad_pcb file
    """
    return json.dumps(pcb_file.get_pcb_tracks(filepath), indent=2)


@mcp.tool()
def get_pcb_zones_from_file(filepath: str) -> str:
    """Get all copper zones in a PCB file.

    Args:
        filepath: Full path to the .kicad_pcb file
    """
    return json.dumps(pcb_file.get_pcb_zones(filepath), indent=2)


@mcp.tool()
def get_pcb_layers_from_file(filepath: str) -> str:
    """Get board layer definitions from a PCB file.

    Args:
        filepath: Full path to the .kicad_pcb file
    """
    return json.dumps(pcb_file.get_pcb_layers(filepath), indent=2)


@mcp.tool()
def get_pcb_setup_from_file(filepath: str) -> str:
    """Get board setup (stackup, design rules) from a PCB file.

    Args:
        filepath: Full path to the .kicad_pcb file
    """
    return json.dumps(pcb_file.get_pcb_setup(filepath), indent=2)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
