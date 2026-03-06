"""Item CRUD tools: get, create, update, delete items."""

from google.protobuf.json_format import MessageToDict

from kicad_mcp.connection import get_connection
from kicad_mcp.tools.base import DOCTYPE_MAP

# Import type modules so their descriptors are registered in the protobuf pool.
# This is required for MessageToDict to resolve Any-typed fields.
import kicad_mcp.proto.board.board_types_pb2 as _board_types  # noqa: F401
import kicad_mcp.proto.board.board_pb2 as _board  # noqa: F401
import kicad_mcp.proto.schematic.schematic_types_pb2 as _sch_types  # noqa: F401
import kicad_mcp.proto.common.types.base_types_pb2 as _base_types  # noqa: F401

from kicad_mcp.proto.common.commands.editor_commands_pb2 import (
    BeginCommit, BeginCommitResponse,
    EndCommit, EndCommitResponse,
    GetItems, GetItemsResponse,
    CreateItems, CreateItemsResponse,
    UpdateItems, UpdateItemsResponse,
    DeleteItems, DeleteItemsResponse,
    ParseAndCreateItemsFromString,
)

# Human-readable item type names to KiCadObjectType enum values
ITEM_TYPE_MAP = {
    # PCB types
    "pcb_footprint": 1,
    "pcb_pad": 2,
    "pcb_shape": 3,
    "pcb_reference_image": 4,
    "pcb_field": 5,
    "pcb_generator": 6,
    "pcb_text": 7,
    "pcb_textbox": 8,
    "pcb_table": 9,
    "pcb_tablecell": 10,
    "pcb_track": 11,
    "pcb_via": 12,
    "pcb_arc": 13,
    "pcb_marker": 14,
    "pcb_dimension": 15,
    "pcb_zone": 16,
    "pcb_group": 17,
    # Schematic types
    "sch_marker": 18,
    "sch_junction": 19,
    "sch_no_connect": 20,
    "sch_bus_wire_entry": 21,
    "sch_bus_bus_entry": 22,
    "sch_line": 23,
    "sch_shape": 24,
    "sch_bitmap": 25,
    "sch_textbox": 26,
    "sch_text": 27,
    "sch_table": 28,
    "sch_tablecell": 29,
    "sch_label": 30,
    "sch_global_label": 31,
    "sch_hier_label": 32,
    "sch_directive_label": 33,
    "sch_field": 34,
    "sch_symbol": 35,
    "sch_sheet_pin": 36,
    "sch_sheet": 37,
    "sch_pin": 38,
    "lib_symbol": 39,
}

# Reverse map for display
ITEM_TYPE_NAMES = {v: k for k, v in ITEM_TYPE_MAP.items()}


def _resolve_item_types(item_types: list[str]) -> list[int]:
    result = []
    for t in item_types:
        val = ITEM_TYPE_MAP.get(t.lower())
        if val is None:
            raise ValueError(f"Unknown item type '{t}'. Available: {', '.join(sorted(ITEM_TYPE_MAP.keys()))}")
        result.append(val)
    return result


def get_items(document_type: str, filename: str, item_types: list[str]) -> list[dict]:
    conn = get_connection()
    dt = DOCTYPE_MAP.get(document_type.lower())
    if dt is None:
        raise ValueError(f"Unknown document_type '{document_type}'")

    type_vals = _resolve_item_types(item_types)

    cmd = GetItems()
    cmd.header.document.type = dt
    cmd.header.document.board_filename = filename
    for tv in type_vals:
        cmd.types.append(tv)

    resp = conn.send(cmd, GetItemsResponse)
    return [MessageToDict(item, preserving_proto_field_name=True) for item in resp.items]


def create_items(document_type: str, filename: str, items_kicad_string: str) -> list[dict]:
    """Create items from KiCad s-expression string format."""
    conn = get_connection()
    dt = DOCTYPE_MAP.get(document_type.lower())
    if dt is None:
        raise ValueError(f"Unknown document_type '{document_type}'")

    # Begin commit for undo support
    begin = BeginCommit()
    begin.document.type = dt
    begin.document.board_filename = filename
    commit_resp = conn.send(begin, BeginCommitResponse)

    try:
        cmd = ParseAndCreateItemsFromString()
        cmd.header.document.type = dt
        cmd.header.document.board_filename = filename
        cmd.data = items_kicad_string
        resp = conn.send(cmd, CreateItemsResponse)
        result = [MessageToDict(item, preserving_proto_field_name=True) for item in resp.created_items]

        # Push commit
        end = EndCommit()
        end.commit.id.value = commit_resp.id.value
        end.push = True
        conn.send(end, EndCommitResponse)

        return result
    except Exception:
        # Drop commit on failure
        end = EndCommit()
        end.commit.id.value = commit_resp.id.value
        end.push = False
        try:
            conn.send(end, EndCommitResponse)
        except Exception:
            pass
        raise


def delete_items(document_type: str, filename: str, item_ids: list[str]) -> list[dict]:
    conn = get_connection()
    dt = DOCTYPE_MAP.get(document_type.lower())
    if dt is None:
        raise ValueError(f"Unknown document_type '{document_type}'")

    begin = BeginCommit()
    begin.document.type = dt
    begin.document.board_filename = filename
    commit_resp = conn.send(begin, BeginCommitResponse)

    try:
        cmd = DeleteItems()
        cmd.header.document.type = dt
        cmd.header.document.board_filename = filename
        for item_id in item_ids:
            kiid = cmd.item_ids.add()
            kiid.value = item_id

        resp = conn.send(cmd, DeleteItemsResponse)
        result = [MessageToDict(r, preserving_proto_field_name=True) for r in resp.results]

        end = EndCommit()
        end.commit.id.value = commit_resp.id.value
        end.push = True
        conn.send(end, EndCommitResponse)

        return result
    except Exception:
        end = EndCommit()
        end.commit.id.value = commit_resp.id.value
        end.push = False
        try:
            conn.send(end, EndCommitResponse)
        except Exception:
            pass
        raise
