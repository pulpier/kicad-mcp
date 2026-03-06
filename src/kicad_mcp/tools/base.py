"""Base tools: ping, version, open documents."""

from google.protobuf.json_format import MessageToDict

from kicad_mcp.connection import get_connection
from kicad_mcp.proto.common.commands.base_commands_pb2 import (
    GetVersion, GetVersionResponse,
    Ping,
)
from kicad_mcp.proto.common.commands.editor_commands_pb2 import (
    GetOpenDocuments, GetOpenDocumentsResponse,
)

DOCTYPE_MAP = {"schematic": 1, "pcb": 3}


def ping() -> str:
    conn = get_connection()
    conn.send(Ping(), Ping)
    return "KiCad is running"


def get_version() -> dict:
    conn = get_connection()
    resp = conn.send(GetVersion(), GetVersionResponse)
    return MessageToDict(resp, preserving_proto_field_name=True)


def get_open_documents(document_type: str | None = None) -> list[dict]:
    conn = get_connection()
    results = []

    types_to_query = []
    if document_type is None:
        types_to_query = list(DOCTYPE_MAP.values())
    else:
        dt = DOCTYPE_MAP.get(document_type.lower())
        if dt is None:
            raise ValueError(f"Unknown document_type '{document_type}'. Use 'schematic' or 'pcb'.")
        types_to_query = [dt]

    for dt in types_to_query:
        cmd = GetOpenDocuments()
        cmd.type = dt
        try:
            resp = conn.send(cmd, GetOpenDocumentsResponse)
            for doc in resp.documents:
                results.append(MessageToDict(doc, preserving_proto_field_name=True))
        except Exception:
            pass

    return results
