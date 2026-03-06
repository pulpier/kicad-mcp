"""KiCad IPC API connection via NNG socket."""

import os
import platform
import tempfile

import pynng
from google.protobuf.message import Message

from kicad_mcp.proto.common.envelope_pb2 import ApiRequest, ApiResponse


class KiCadConnectionError(Exception):
    pass


class KiCadApiError(Exception):
    pass


class KiCadConnection:
    """Direct connection to KiCad's IPC API socket."""

    def __init__(self, socket_path: str | None = None, timeout_ms: int = 5000):
        if socket_path is None:
            socket_path = os.environ.get("KICAD_API_SOCKET")
        if socket_path is None:
            if platform.system() == "Windows":
                socket_path = f"ipc://{os.path.join(tempfile.gettempdir(), 'kicad', 'api.sock')}"
            else:
                socket_path = "ipc:///tmp/kicad/api.sock"

        self._socket_path = socket_path
        self._timeout_ms = timeout_ms
        self._conn: pynng.Req0 | None = None

    def _ensure_connected(self):
        if self._conn is not None:
            return
        try:
            self._conn = pynng.Req0(
                dial=self._socket_path,
                block_on_dial=True,
                send_timeout=self._timeout_ms,
                recv_timeout=self._timeout_ms,
            )
        except pynng.exceptions.NNGException as e:
            raise KiCadConnectionError(f"Failed to connect to KiCad at {self._socket_path}: {e}") from None

    def send(self, command: Message, response_type: type) -> Message:
        """Send a protobuf command and return the typed response."""
        self._ensure_connected()

        req = ApiRequest()
        req.header.client_name = "kicad-mcp"
        req.message.Pack(command)

        try:
            self._conn.send(req.SerializeToString())
            raw = self._conn.recv()
        except pynng.exceptions.NNGException as e:
            self._conn = None
            raise KiCadConnectionError(f"Communication error: {e}") from None

        api_resp = ApiResponse()
        api_resp.ParseFromString(raw)

        # AS_OK = 1; anything else is an error
        if api_resp.status.status != 1:
            status_names = {
                0: "UNKNOWN", 2: "TIMEOUT", 3: "BAD_REQUEST",
                4: "NOT_READY", 5: "UNHANDLED", 6: "TOKEN_MISMATCH",
                7: "BUSY", 8: "UNIMPLEMENTED",
            }
            status_name = status_names.get(api_resp.status.status, str(api_resp.status.status))
            raise KiCadApiError(f"[{status_name}] {api_resp.status.error_message}")

        result = response_type()
        api_resp.message.Unpack(result)
        return result

    def close(self):
        if self._conn is not None:
            self._conn.close()
            self._conn = None


# Singleton connection
_connection: KiCadConnection | None = None


def get_connection() -> KiCadConnection:
    global _connection
    if _connection is None:
        _connection = KiCadConnection()
    return _connection
