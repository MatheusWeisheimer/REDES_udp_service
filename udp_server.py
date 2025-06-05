import socket
import struct
import logging
from typing import Tuple, List

FLAGS_SIZE = 3  # bytes
DOUBLE_SIZE = 8  # bytes

def parse_packet(data: bytes) -> Tuple[Tuple[int, int, int], List[float]]:
    if len(data) < FLAGS_SIZE:
        raise ValueError("Received data too short")
    flags = struct.unpack('3B', data[:FLAGS_SIZE])
    doubles = []
    if len(data) > FLAGS_SIZE:
        doubles_bytes = data[FLAGS_SIZE:]
        if len(doubles_bytes) % DOUBLE_SIZE != 0:
            raise ValueError("Malformed packet: doubles section not a multiple of 8 bytes")
        n_doubles = len(doubles_bytes) // DOUBLE_SIZE
        doubles = list(struct.unpack(f'{n_doubles}d', doubles_bytes))
    return flags, doubles

def start_udp_server(host: str = '0.0.0.0', port: int = 2022) -> None:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind((host, port))
        logging.info(f"UDP server listening on {host}:{port}")

        while True:
            try:
                data, addr = sock.recvfrom(4096)
                flags, doubles = parse_packet(data)
                logging.info(f"Flags: {flags}, Doubles: {doubles} from {addr}")

                response_bytes = b''
                if flags[0]:
                    response_bytes += struct.pack('d', sum(doubles))
                if flags[1]:
                    avg = sum(doubles) / len(doubles) if doubles else 0
                    response_bytes += struct.pack('d', avg)
                if flags[2]:
                    if doubles:
                        response_bytes += struct.pack('2d', min(doubles), max(doubles))
                    else:
                        response_bytes += struct.pack('2d', float('nan'), float('nan'))

                sock.sendto(response_bytes, addr)
            except ValueError as ve:
                logging.warning(f"Packet error from {addr}: {ve}")
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
    except KeyboardInterrupt:
        logging.info("Server shutting down (KeyboardInterrupt)")
    finally:
        sock.close()
        logging.info("Socket closed")

if __name__ == "__main__":
    start_udp_server()