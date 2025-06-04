import socket
import struct

def start_udp_server(host='127.0.0.1', port=2022):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f"UDP server listening on {host}:{port}")

    while True:
        data, addr = sock.recvfrom(4096)
        if len(data) < 3:
            print("Received data too short")
            continue

        flags = struct.unpack('3B', data[:3])
        doubles = []
        if len(data) > 3:
            n_doubles = (len(data) - 3) // 8
            doubles = list(struct.unpack(f'{n_doubles}d', data[3:3 + n_doubles * 8]))

        print(f"Flags: {flags}, Doubles: {doubles} from {addr}")

        response_bytes = b''
        if flags[0]:  # sum
            response_bytes += struct.pack('d', sum(doubles))
        if flags[1]:  # average
            avg = sum(doubles) / len(doubles) if doubles else 0
            response_bytes += struct.pack('d', avg)
        if flags[2]:  # minMax
            if doubles:
                response_bytes += struct.pack('2d', min(doubles), max(doubles))
            else:
                response_bytes += struct.pack('2d', float('nan'), float('nan'))

        sock.sendto(response_bytes, addr)

if __name__ == "__main__":
    start_udp_server() 