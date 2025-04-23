# udp_utils.py

import os
import socket
import sys
import signal
import datetime
import json
import time
from pathlib import Path

# --- File Paths ---
CONFIG_FILE = "udp_config.json"
META_PATH = Path("command.meta.json")
COMMANDS_FOLDER = "commands"

# --- Defaults ---
DEFAULT_DELAY = 2
DEFAULT_MODE = "UDP"
DEFAULT_PARSER = "text"

# --- Supported Options ---
SUPPORTED_MODES = ["UDP", "SPI", "I2C"]
SUPPORTED_PARSERS = ["text", "hex", "json"]

# --- Runtime State ---
CURRENT_SUBFOLDER = ""

LOG_FILE = "received_packets.log"

def start_receive_mode(listen_ip="0.0.0.0", listen_port=5005):
    print(f"\n📡 Listening for UDP packets on {listen_ip}:{listen_port} ... (Press Ctrl+C to stop)\n")

    running = True

    def handle_sigint(sig, frame):
        nonlocal running
        running = False
        print("\n🛑 Receive mode interrupted. Exiting...\n")

    signal.signal(signal.SIGINT, handle_sigint)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock, open(LOG_FILE, "a") as log_file:
        sock.bind((listen_ip, listen_port))
        sock.settimeout(1.0)  # ⏱️ Prevents blocking forever

        while running:
            try:
                data, addr = sock.recvfrom(4096)
                timestamp = datetime.datetime.now().isoformat(timespec='seconds')
                hex_data = data.hex(' ')
                message = f"[{timestamp}] From {addr[0]}:{addr[1]} | {hex_data}"

                print(message)
                log_file.write(message + "\n")
                log_file.flush()
            except socket.timeout:
                continue  # 🔁 check if still running
            except Exception as e:
                print(f"❌ Error during receive: {e}")
                break


# --- Meta Config Helpers ---
def load_meta_config():
    if META_PATH.exists():
        return json.loads(META_PATH.read_text(encoding="utf-8"))
    return {}

def save_meta_config(config):
    META_PATH.write_text(json.dumps(config, indent=2), encoding="utf-8")

# --- Meta Getters/Setters ---
def get_mode():
    return load_meta_config().get("mode", DEFAULT_MODE)

def set_mode(mode):
    if mode not in SUPPORTED_MODES:
        raise ValueError(f"Unsupported mode: {mode}")
    config = load_meta_config()
    config["mode"] = mode
    save_meta_config(config)

def get_parser_type():
    return load_meta_config().get("parser", DEFAULT_PARSER)

def set_parser_type(parser):
    if parser not in SUPPORTED_PARSERS:
        raise ValueError(f"Unsupported parser type: {parser}")
    config = load_meta_config()
    config["parser"] = parser
    save_meta_config(config)

def load_command_subfolder():
    return load_meta_config().get("command_folder", "")

def set_command_subfolder(name, persist=False):
    global CURRENT_SUBFOLDER
    CURRENT_SUBFOLDER = name
    if persist:
        config = load_meta_config()
        config["command_folder"] = name
        save_meta_config(config)

# --- Delay (udp_config.json) ---
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    return {}

def save_config(udp_ip, udp_port):
    config = load_config()
    config["udp_ip"] = udp_ip
    config["udp_port"] = udp_port
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file)

def load_delay():
    config = load_config()
    return config.get("delay", DEFAULT_DELAY)

def save_delay(delay):
    config = load_config()
    config["delay"] = delay
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file)

# --- Folder Management ---
def get_active_folder():
    return os.path.join(COMMANDS_FOLDER, CURRENT_SUBFOLDER)

def list_subfolders():
    if not os.path.exists(COMMANDS_FOLDER):
        os.makedirs(COMMANDS_FOLDER)
    return [
        name for name in os.listdir(COMMANDS_FOLDER)
        if os.path.isdir(os.path.join(COMMANDS_FOLDER, name))
    ]

def list_files():
    folder = get_active_folder()
    if not os.path.exists(folder):
        os.makedirs(folder)
    return [
        f for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f))
    ]

# --- Command Sending (UDP only for now) ---
def send_udp_command(file_name, udp_ip, udp_port, delay):
    parser = get_parser_type()
    try:
        file_path = os.path.join(get_active_folder(), file_name)
        with open(file_path, 'r') as file:
            lines = [
                line.strip()
                for line in file.readlines()
                if line.strip() and not line.strip().startswith('#')
            ]

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        for line in lines:
            if parser == "text":
                payload = line.encode()
            elif parser == "hex":
                payload = bytes.fromhex(line.replace(",", " "))
            elif parser == "json":
                payload = json.dumps(json.loads(line)).encode("utf-8")
            else:
                raise ValueError(f"Unsupported parser: {parser}")

            sock.sendto(payload, (udp_ip, udp_port))
            print(f"Sent [{parser}]: {line}")
            time.sleep(delay)

        print(f"Finished sending data from {file_name} to {udp_ip}:{udp_port}")
        sock.close()
    except Exception as e:
        print(f"Error sending UDP data: {e}")

def send_all_files(udp_ip, udp_port, delay):
    files = list_files()
    if not files:
        print("No command files found.")
        return
    for file in files:
        print(f"Sending file: {file}")
        send_udp_command(file, udp_ip, udp_port, delay)

def send_cmd_list(file_name, udp_ip, udp_port, delay):
    print(f"Processing CMD file: {file_name}")
    try:
        cmd_path = os.path.join(get_active_folder(), file_name)
        with open(cmd_path, 'r') as file:
            command_files = [
                line.strip()
                for line in file.readlines()
                if line.strip() and not line.strip().startswith('#')
            ]
        for cmd_file in command_files:
            full_path = os.path.join(get_active_folder(), cmd_file)
            if os.path.exists(full_path):
                print(f"Executing commands from {cmd_file}...")
                send_udp_command(cmd_file, udp_ip, udp_port, delay)
            else:
                print(f"Warning: Command file {cmd_file} not found.")
    except Exception as e:
        print(f"Error processing CMD file: {e}")
