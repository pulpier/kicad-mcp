"""Board/PCB-specific tools."""

from google.protobuf.json_format import MessageToDict

from kicad_mcp.connection import get_connection
from kicad_mcp.proto.board.board_commands_pb2 import (
    GetBoardStackup, BoardStackupResponse,
    GetNets, NetsResponse,
    GetNetClassForNets, NetClassForNetsResponse,
    GetBoardOrigin, SetBoardOrigin,
    GetBoardEnabledLayers, BoardEnabledLayersResponse,
    GetActiveLayer, SetActiveLayer, BoardLayerResponse,
    GetVisibleLayers, BoardLayers,
    SetVisibleLayers,
    RefillZones,
    GetBoardEditorAppearanceSettings, BoardEditorAppearanceSettings,
)
from kicad_mcp.proto.common.types.base_types_pb2 import Vector2

# Import board types for Any field resolution
import kicad_mcp.proto.board.board_types_pb2 as _bt  # noqa: F401
import kicad_mcp.proto.board.board_pb2 as _b  # noqa: F401


def _set_board(msg, filename: str):
    """Set document specifier for board commands."""
    msg.type = 3  # DOCTYPE_PCB
    msg.board_filename = filename


def get_board_stackup(filename: str) -> dict:
    conn = get_connection()
    cmd = GetBoardStackup()
    _set_board(cmd.board, filename)
    resp = conn.send(cmd, BoardStackupResponse)
    return MessageToDict(resp, preserving_proto_field_name=True)


def get_nets(filename: str) -> list[dict]:
    conn = get_connection()
    cmd = GetNets()
    _set_board(cmd.board, filename)
    resp = conn.send(cmd, NetsResponse)
    return [MessageToDict(net, preserving_proto_field_name=True) for net in resp.nets]


def get_net_class_for_nets(net_names: list[str]) -> dict:
    conn = get_connection()
    cmd = GetNetClassForNets()
    for name in net_names:
        net = cmd.net.add()
        net.name = name
    resp = conn.send(cmd, NetClassForNetsResponse)
    return MessageToDict(resp, preserving_proto_field_name=True)


def get_board_origin(filename: str) -> dict:
    conn = get_connection()
    cmd = GetBoardOrigin()
    _set_board(cmd.board, filename)
    resp = conn.send(cmd, Vector2)
    return MessageToDict(resp, preserving_proto_field_name=True)


def set_board_origin(filename: str, x_mm: float, y_mm: float) -> str:
    conn = get_connection()
    cmd = SetBoardOrigin()
    _set_board(cmd.board, filename)
    cmd.origin.x_nm = int(x_mm * 1_000_000)
    cmd.origin.y_nm = int(y_mm * 1_000_000)
    conn.send(cmd, SetBoardOrigin)
    return f"Board origin set to ({x_mm}, {y_mm}) mm"


def get_enabled_layers(filename: str) -> dict:
    conn = get_connection()
    cmd = GetBoardEnabledLayers()
    _set_board(cmd.board, filename)
    resp = conn.send(cmd, BoardEnabledLayersResponse)
    return MessageToDict(resp, preserving_proto_field_name=True)


def get_active_layer(filename: str) -> dict:
    conn = get_connection()
    cmd = GetActiveLayer()
    _set_board(cmd.board, filename)
    resp = conn.send(cmd, BoardLayerResponse)
    return MessageToDict(resp, preserving_proto_field_name=True)


def set_active_layer(filename: str, layer: int) -> str:
    conn = get_connection()
    cmd = SetActiveLayer()
    _set_board(cmd.board, filename)
    cmd.layer = layer
    conn.send(cmd, SetActiveLayer)
    return f"Active layer set to {layer}"


def refill_zones(filename: str) -> str:
    conn = get_connection()
    cmd = RefillZones()
    _set_board(cmd.board, filename)
    conn.send(cmd, RefillZones)
    return "Zones refilled"


def get_board_appearance() -> dict:
    conn = get_connection()
    resp = conn.send(GetBoardEditorAppearanceSettings(), BoardEditorAppearanceSettings)
    return MessageToDict(resp, preserving_proto_field_name=True)
