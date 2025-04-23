import json
import os
import socket

_KOL_CODE = bytearray(b"\x6b\x6f\x6c\x63\x6f\x64\x65\x00")
_KOL_EXIT = bytearray(b"\x6b\x6f\x6c\x65\x78\x69\x74\x00")
_KOL_RESP = bytearray(b"\x6b\x6f\x6c\x72\x65\x73\x70\x00")


class KolConn:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.hostname, self.port))

    def __repr__(self):
        return f"KolConn(hostname='{self.hostname}', port='{self.port}')"

    def _send(self, cmd):
        if self.sock is None:
            raise Exception("Cannot send on a closed socket.")
        utf8 = cmd.encode("utf-8")
        msg_len = len(utf8)
        self.sock.send(_KOL_CODE)
        self.sock.send(msg_len.to_bytes(8, "little"))
        self.sock.send(utf8)

    def _recv(self):
        if self.sock is None:
            raise Exception("Cannot receive on a closed socket.")
        kol_resp = self.sock.recv(8)
        if kol_resp != _KOL_RESP:
            raise Exception(
                f"Expecting the magic number {_KOL_RESP}, got: {kol_resp}"
            )
        size_bytes_le = self.sock.recv(8)
        size = int.from_bytes(size_bytes_le, byteorder="little", signed=False)
        data = bytearray()
        n = size
        while len(data) < n:
            packet = self.sock.recv(n - len(data))
            if not packet:
                raise Exception("Received no data from kol.")
            data.extend(packet)
        return data.decode("utf-8")

    def run_command(self, cmd):
        self._send(cmd)
        reply = self._recv()
        return reply

    def to_json(self, table, cell_begin, cell_end):
        kql = f"get ${table}[{cell_begin}:{cell_end}];"
        res = self.run_command(kql)
        return json.loads(res)

    def to_numpy(self, table, cell_begin, cell_end, dtype=None):
        import numpy as np

        res = self.to_json(table, cell_begin, cell_end)
        if dtype is None:
            a = np.array(res)
        else:
            a = np.array(res, dtype=dtype)
        return a

    def to_pandas(self, table, cell_begin, cell_end, header=None):
        import pandas as pd

        j = self.to_json(table, cell_begin, cell_end)
        if len(j) == 0:
            return pd.DataFrame()
        if header is not None and isinstance(j[0], list):
            data = {}
            for heading, col in zip(header, j):
                data[heading] = col
            return pd.DataFrame(data)
        if header is not None:
            return pd.DataFrame({header[0]: j})
        if isinstance(j[0], list):
            data = {col[0]: col[1:] for col in j}
            df = pd.DataFrame(data)
            return df
        else:
            data = {j[0]: j[1:]}
            df = pd.DataFrame(data)
            return df

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        if self.sock is not None:
            self.sock.send(_KOL_EXIT)
            self.sock.close()
            self.sock = None


def connect(hostname=None, port=None):
    if hostname is None:
        env_host = os.getenv("KOL_HOST")
        if env_host is not None:
            hostname = env_host

    if port is None:
        env_port = os.getenv("KOL_PORT")
        if env_port is not None:
            port = int(env_port)

    if hostname is None:
        hostname = "localhost"
    if port is None:
        port = 7890

    try:
        conn = KolConn(hostname=hostname, port=port)
    except Exception as excp:
        raise Exception(
            f"failed to connect to kol using hostname={hostname}, port={port}: {excp}"
        )
    return conn
