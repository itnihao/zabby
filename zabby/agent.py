import struct
from six.moves import socketserver
from zabby.utils import b

__PROTOCOL__ = None
__DATA_SOURCE__ = None


def set_protocol(protocol):
    """
    Sets the protocol that will be used by request handler
    """
    global __PROTOCOL__
    __PROTOCOL__ = protocol


def set_data_source(data_source):
    """
    Sets the data_source that will be used by request handler
    """
    global __DATA_SOURCE__
    __DATA_SOURCE__ = data_source


def get_protocol():
    """
    Returns protocol set by set_protocol
    """
    return __PROTOCOL__


def get_data_source():
    """
    Returns data_source set by set_data_source
    """
    return __DATA_SOURCE__


class AgentRequestHandler(socketserver.BaseRequestHandler):
    """
    This class is a proxy for protocol interaction and data retrieval
    It should be used with socketserver.TCPServer
    """

    def setup(self):
        self.protocol = get_protocol()
        self.data_source = get_data_source()

    def handle(self):
        key = self.protocol.receive_key(self.request)
        response = self.data_source.process(key)
        self.protocol.send_response(self.request, response)


class ZBXDProtocol():
    MAX_KEY_LENGTH = 1024
    HEADER = b'ZBXD\1'
    HEADER_LENGTH = 5
    EXPECTED_LENGTH_SIZE = 8
    RESPONSE_FORMAT = "<5sq{data_length}s"

    def receive_key(self, client):
        """
        Receives key and returns it

        Expects to receive header followed by the length of the key
        followed by the key. If header is not received tries to get up to
        MAX_KEY_LENGTH bytes.
        """
        received = client.recv(self.HEADER_LENGTH)
        if received == self.HEADER:
            expected_length = struct.unpack(
                'q', client.recv(self.EXPECTED_LENGTH_SIZE)
            )[0]
            key = client.recv(expected_length)
        else:
            key = received + client.recv(self.MAX_KEY_LENGTH)
        return key.decode('utf-8')

    def _calculate_response(self, value):
        data_length = len(str(value))
        response = struct.pack(
            self.RESPONSE_FORMAT.format(data_length=data_length),
            self.HEADER,
            data_length,
            b(str(value))
        )
        return response

    def send_response(self, client, value):
        """
        Formats value according to protocol and sends it to client
        """
        response = self._calculate_response(value)
        client.sendall(response)