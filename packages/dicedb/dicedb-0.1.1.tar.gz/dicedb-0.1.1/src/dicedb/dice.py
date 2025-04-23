"""DiceDB client."""

import socket
import uuid

from . import const
from .commands import DiceCommands
from .exceptions import (
    DiceConnectionError,
    DiceSendCommandError,
    DiceResponseTooLargeError
)
from .proto.cmd_pb2 import Command
from .proto.res_pb2 import Result
from .utils.response_deserializer import deserialize


class Dice(DiceCommands):
    """An synchronous client for DiceDB."""

    def __init__(self, host: str, port: int, timeout: float = 5.0, try_to_convert: bool = False) -> None:
        """Initialize the Dice client.

        Args:
            host (str): DiceDB server host
            port (int): DiceDB server port
            timeout (float): Connection timeout in seconds
            try_to_convert (bool): Convert the response type if server response value is string-int
        """
        self._host = host
        self._port = port
        self._timeout = timeout
        self._socket = None
        self._connected: bool = False
        self._try_to_convert: bool = try_to_convert
        self._client_id = str(uuid.uuid4())
        self._connect()
        self._do_handshake()

    def _connect(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(self._timeout)
        try:
            self._socket.connect((self._host, self._port))
            self._connected = True
        except socket.timeout:
            raise DiceConnectionError(
                f'Connection to {self._host}:{self._port} timed out'
            )
        except ConnectionRefusedError:
            raise DiceConnectionError(
                f'Connection to {self._host}:{self._port} was refused'
            )
        except OSError as e:
            raise DiceConnectionError(
                f'Failed to connect to {self._host}:{self._port}: {e}'
            ) from e

    def _do_handshake(self):
        self._handshake(self._client_id)

    def _fire(self, cmd: str, *args):
        if not self._connected:
            raise DiceConnectionError('Not connected to the server.')

        current_command = self._build_command(cmd, *args)

        self._send_command(current_command)
        result = self._read_response_and_parse()
        return deserialize(result, try_to_convert=self._try_to_convert)

    @staticmethod
    def _build_command(cmd: str, *args) -> Command:
        """Build a command protobuf object.

        Args:
            cmd (str): The command to be executed.
            *args: The arguments for the command.

        Returns:
            Command: The built command object.
        """
        command = Command()
        command.cmd = cmd
        command.args.extend([str(arg) for arg in args])
        return command

    def _send_command(self, cmd: Command):
        byte_string = cmd.SerializeToString()
        try:
            self._socket.sendall(byte_string)
        except OSError as e:
            raise DiceSendCommandError('Failed to send command') from e

    def _read_response_and_parse(self) -> Result:
        buffer = bytearray(const.MAX_REQUEST_SIZE)
        mv = memoryview(buffer)
        received_bytes_size = 0

        while True:
            chunk_view = mv[
                received_bytes_size : received_bytes_size
                + const.IO_BUFFER_SIZE
            ]
            nbytes = self._socket.recv_into(chunk_view)

            if not nbytes:
                break

            received_bytes_size += nbytes
            if received_bytes_size > const.MAX_REQUEST_SIZE:
                raise DiceResponseTooLargeError(
                    f'Response too large: {received_bytes_size} bytes'
                )

            if nbytes < const.IO_BUFFER_SIZE:
                break

        result = Result()
        result.ParseFromString(mv[:received_bytes_size])
        return result

    def close(self):
        """Close the connection to the server.

        Returns:
            None
        """
        if self._socket and self._connected:
            self._socket.close()
            self._connected = False

    def __enter__(self):
        """Enter method for the context manager.

        Returns:
            `Dice`
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit method for the context manager.

        Returns:
            None
        """
        self.close()