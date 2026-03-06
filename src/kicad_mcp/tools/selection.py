"""Selection tools: get, add, remove, clear, hit test."""

from google.protobuf.json_format import MessageToDict

from kicad_mcp.connection import get_connection
from kicad_mcp.proto.common.commands.editor_commands_pb2 import (
    GetSelection, SelectionResponse,
    SaveSelectionToString, SavedSelectionResponse,
    AddToSelection,
    RemoveFromSelection,
    ClearSelection,
    HitTest, HitTestResponse,
)


def get_selection() -> list[dict]:
    conn = get_connection()
    resp = conn.send(GetSelection(), SelectionResponse)
    return [MessageToDict(item, preserving_proto_field_name=True) for item in resp.items]


def get_selection_as_string() -> str:
    conn = get_connection()
    resp = conn.send(SaveSelectionToString(), SavedSelectionResponse)
    return resp.contents


def add_to_selection(item_ids: list[str]) -> str:
    conn = get_connection()
    cmd = AddToSelection()
    for item_id in item_ids:
        kiid = cmd.item_ids.add()
        kiid.value = item_id
    conn.send(cmd, AddToSelection)
    return f"Added {len(item_ids)} items to selection"


def remove_from_selection(item_ids: list[str]) -> str:
    conn = get_connection()
    cmd = RemoveFromSelection()
    for item_id in item_ids:
        kiid = cmd.item_ids.add()
        kiid.value = item_id
    conn.send(cmd, RemoveFromSelection)
    return f"Removed {len(item_ids)} items from selection"


def clear_selection() -> str:
    conn = get_connection()
    conn.send(ClearSelection(), ClearSelection)
    return "Selection cleared"


def hit_test(x: float, y: float, tolerance: float = 0.0) -> list[dict]:
    conn = get_connection()
    cmd = HitTest()
    cmd.position.x_nm = int(x * 1_000_000)
    cmd.position.y_nm = int(y * 1_000_000)
    if tolerance > 0:
        cmd.tolerance = int(tolerance * 1_000_000)
    resp = conn.send(cmd, HitTestResponse)
    return [MessageToDict(item, preserving_proto_field_name=True) for item in resp.items]
