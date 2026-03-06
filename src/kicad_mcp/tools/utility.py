"""Utility tools: text extents, text as shapes, run action."""

from google.protobuf.json_format import MessageToDict

from kicad_mcp.connection import get_connection
from kicad_mcp.proto.common.commands.base_commands_pb2 import (
    GetTextExtents, GetTextAsShapes, GetTextAsShapesResponse,
)
from kicad_mcp.proto.common.commands.editor_commands_pb2 import (
    RunAction, RunActionResponse,
)
from kicad_mcp.proto.common.types.base_types_pb2 import (
    Text, TextAttributes,
)


def get_text_extents(text: str, font_size_mm: float = 1.27, bold: bool = False, italic: bool = False) -> dict:
    conn = get_connection()
    cmd = GetTextExtents()
    cmd.text.text = text
    cmd.text.attributes.size.x_nm = int(font_size_mm * 1_000_000)
    cmd.text.attributes.size.y_nm = int(font_size_mm * 1_000_000)
    cmd.text.attributes.bold = bold
    cmd.text.attributes.italic = italic
    from kicad_mcp.proto.common.types.base_types_pb2 import Box2
    resp = conn.send(cmd, Box2)
    return MessageToDict(resp, preserving_proto_field_name=True)


def get_text_as_shapes(text: str, font_size_mm: float = 1.27, bold: bool = False, italic: bool = False) -> dict:
    conn = get_connection()
    cmd = GetTextAsShapes()
    entry = cmd.text.add()
    entry.text.text = text
    entry.text.attributes.size.x_nm = int(font_size_mm * 1_000_000)
    entry.text.attributes.size.y_nm = int(font_size_mm * 1_000_000)
    entry.text.attributes.bold = bold
    entry.text.attributes.italic = italic
    resp = conn.send(cmd, GetTextAsShapesResponse)
    return MessageToDict(resp, preserving_proto_field_name=True)


def run_action(action: str) -> dict:
    conn = get_connection()
    cmd = RunAction()
    cmd.action = action
    resp = conn.send(cmd, RunActionResponse)
    return MessageToDict(resp, preserving_proto_field_name=True)
