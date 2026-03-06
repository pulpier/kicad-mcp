"""Project tools: net classes, text variables."""

from google.protobuf.json_format import MessageToDict

from kicad_mcp.connection import get_connection
from kicad_mcp.proto.common.commands.project_commands_pb2 import (
    GetNetClasses, NetClassesResponse,
    GetTextVariables, SetTextVariables,
    ExpandTextVariables, ExpandTextVariablesResponse,
)


def get_net_classes() -> dict:
    conn = get_connection()
    resp = conn.send(GetNetClasses(), NetClassesResponse)
    return MessageToDict(resp, preserving_proto_field_name=True)


def get_text_variables() -> dict:
    conn = get_connection()
    resp = conn.send(GetTextVariables(), SetTextVariables)
    return MessageToDict(resp, preserving_proto_field_name=True)


def set_text_variables(variables: dict[str, str]) -> str:
    conn = get_connection()
    cmd = SetTextVariables()
    for key, value in variables.items():
        cmd.variables[key] = value
    conn.send(cmd, SetTextVariables)
    return f"Set {len(variables)} text variable(s)"


def expand_text_variables(document_type: str, filename: str, text: str) -> str:
    from kicad_mcp.tools.base import DOCTYPE_MAP
    conn = get_connection()
    dt = DOCTYPE_MAP.get(document_type.lower())
    if dt is None:
        raise ValueError(f"Unknown document_type '{document_type}'")

    cmd = ExpandTextVariables()
    cmd.document.type = dt
    cmd.document.board_filename = filename
    cmd.text.text = text
    resp = conn.send(cmd, ExpandTextVariablesResponse)
    return resp.text.text
