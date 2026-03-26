import socket
import struct
import argparse

MAX_FRAME_SIZE = 1024  # Adjust as needed

def send_frame_and_wait_for_response(ip, port, payload):
    length = len(payload)
    header = struct.pack('<BH', 0x3c, length)
    frame = header + payload.encode('utf-8')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        s.sendall(frame)

        # Wait for response
        response_header = s.recv(3)  # 1 byte type + 2 bytes length
        if len(response_header) != 3:
            print("Error: Incomplete response header")
            return

        response_type, response_length = struct.unpack('<BH', response_header)
        response_payload = s.recv(response_length).decode('utf-8')

        print(f"{payload}: {response_payload}")

def main():
    parser = argparse.ArgumentParser(description='Send a TCP frame with a string payload and wait for a response.')
    parser.add_argument('--ip', required=True, help='Target IP address')
    parser.add_argument('--port', type=int, required=True, help='Target port')
    parser.add_argument('--payload', required=True, help='String payload to send')

    args = parser.parse_args()

    if args.payload == "status":
        for cmd in ["board", "ver", "get name", "get radio", "get lat", "get lon","get owner.info", "get public.key", "get repeat", "get role","get txdelay", "get rxdelay", "get af", "get multi.acks", "region", "get path.hash.mode", "stats-core", "stats-packets", "stats-radio"]:
            send_frame_and_wait_for_response(args.ip, args.port, cmd)
    else:
        send_frame_and_wait_for_response(args.ip, args.port, args.payload)

if __name__ == "__main__":
    main()
