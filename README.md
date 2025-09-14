MP3 Reverse Shell with LSB Steganography
This project is a Python-based tool designed for red teaming in controlled lab environments. It embeds a reverse shell payload with data exfiltration capabilities into an MP3 file using Least Significant Bit (LSB) steganography. The embedded payload, when executed on a target system, establishes a reverse shell connection to an attacker's listener and exfiltrates files from a specified directory.
Author: Taylor Christian NewsomeWarning: This tool is for authorized use only in lab environments or with explicit permission. Unauthorized use is illegal and unethical.
Features

LSB Steganography: Embeds a Python reverse shell payload into an MP3 file without significantly affecting its playability.
Reverse Shell: Establishes a connection back to the attacker's listener, providing an interactive shell (/bin/sh).
Data Exfiltration: Extracts files from a specified directory (default: /tmp) and sends them to the attacker using base64 encoding.
Listener: Includes a server to receive exfiltrated data and interact with the reverse shell.
Error Handling: Robust validation for IP, port, file existence, and payload size.

Requirements
The core script uses Python standard libraries (os, socket, struct, glob, base64). Optional dependencies for enhanced functionality are listed in requirements.txt:
# requirements.txt
pyarmor>=8.5.12  # For payload obfuscation (optional)
pytest>=8.3.2    # For unit testing (optional)

Install optional dependencies:
pip install -r requirements.txt

Usage
This tool is intended for controlled lab environments (e.g., virtual machines). Follow these steps:
1. Setup

Ensure Python 3.6+ is installed.
Place an input.mp3 file in the project directory.
Update the following variables in main.py:
target_ip: Attacker's IP address (e.g., 192.168.1.10).
target_port: Listener port (e.g., 4444).
exfil_dir: Directory to exfiltrate files from (e.g., /tmp).



2. Embed Payload
Run the script to embed the payload into the MP3:
python main.py

This generates output.mp3 with the embedded payload.
3. Start Listener
On the attacker's machine, start the listener to receive exfiltrated data and the reverse shell:
# In main.py, uncomment and run:
start_listener("192.168.1.10", 4444)

Alternatively, use netcat:
nc -lvnp 4444

Exfiltrated files are saved to exfiltrated_data.txt.
4. Deploy and Execute on Target

Transfer output.mp3 to the target system (e.g., via social engineering or file sharing in the lab).
Extract and execute the payload on the target (requires a separate script or manual execution):from main import extract_payload, execute_payload
payload = extract_payload('output.mp3')
execute_payload(payload)

Note: You may need a delivery mechanism (e.g., a fake MP3 player script) to trigger execution.

5. Receive Data
The listener receives base64-encoded files from the target directory and provides an interactive shell.
Notes

MP3 Compatibility: LSB steganography may cause minor audio distortion. Test with a small MP3 file. Consider WAV files for better reliability, as MP3 compression can corrupt payloads.
Execution: The script does not auto-execute the payload on the target. Implement a trigger mechanism suitable for your lab scenario.
Security: Antivirus or EDR tools may detect the payload or modified MP3. Use pyarmor for obfuscation if needed.
Lab Safety: Use in an isolated environment (e.g., VMs with no external network access except to the listener).

Ethical Considerations
This tool is for educational and authorized red teaming purposes only. Unauthorized deployment of reverse shells or data exfiltration is illegal and unethical. Always obtain explicit, written permission from system owners before testing.
Files

main.py: Core script for embedding, extracting, and executing the payload, plus the listener.
requirements.txt: Lists optional dependencies (pyarmor, pytest).

License
This project is provided as-is for educational purposes. The author is not responsible for misuse. Use responsibly and legally.
Contact
For issues or contributions, open a GitHub issue or pull request at https://github.com/SleepTheGod/Mp3-Reverse-Shell/.
© 2025 SleepTheGod
