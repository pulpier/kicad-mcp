"""Document tools: save, revert, export, title block."""

from google.protobuf.json_format import MessageToDict

from kicad_mcp.connection import get_connection
from kicad_mcp.tools.base import DOCTYPE_MAP
from kicad_mcp.proto.common.commands.editor_commands_pb2 import (
    SaveDocument, SaveOptions,
    SaveCopyOfDocument,
    RevertDocument,
    SaveDocumentToString, SavedDocumentResponse,
    GetTitleBlockInfo,
)
from kicad_mcp.proto.common.types.base_types_pb2 import TitleBlockInfo


def _set_doc(msg, document_type: str, filename: str):
    dt = DOCTYPE_MAP.get(document_type.lower())
    if dt is None:
        raise ValueError(f"Unknown document_type '{document_type}'")
    msg.type = dt
    msg.board_filename = filename


def save_document(document_type: str, filename: str) -> str:
    conn = get_connection()
    cmd = SaveDocument()
    _set_doc(cmd.document, document_type, filename)
    conn.send(cmd, SaveDocument)
    return "Document saved"


def save_document_copy(document_type: str, filename: str, new_path: str) -> str:
    conn = get_connection()
    cmd = SaveCopyOfDocument()
    _set_doc(cmd.document, document_type, filename)
    cmd.new_path = new_path
    conn.send(cmd, SaveCopyOfDocument)
    return "Copy saved"


def revert_document(document_type: str, filename: str) -> str:
    conn = get_connection()
    cmd = RevertDocument()
    _set_doc(cmd.document, document_type, filename)
    conn.send(cmd, RevertDocument)
    return "Document reverted"


def get_document_as_string(document_type: str, filename: str) -> str:
    conn = get_connection()
    cmd = SaveDocumentToString()
    _set_doc(cmd.document, document_type, filename)
    resp = conn.send(cmd, SavedDocumentResponse)
    return resp.contents


def get_title_block_info(document_type: str, filename: str) -> dict:
    conn = get_connection()
    cmd = GetTitleBlockInfo()
    _set_doc(cmd.document, document_type, filename)
    resp = conn.send(cmd, TitleBlockInfo)
    return MessageToDict(resp, preserving_proto_field_name=True)
