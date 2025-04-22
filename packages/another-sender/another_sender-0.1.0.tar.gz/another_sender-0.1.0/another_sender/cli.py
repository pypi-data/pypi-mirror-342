# cli.py

import os
import sys
import argparse

from another_sender import __version__
from another_sender.udp_utils import (
    load_config,
    save_config,
    load_delay,
    save_delay,
    list_files,
    list_subfolders,
    set_command_subfolder,
    load_command_subfolder,
    get_active_folder,
    get_mode,
    set_mode,
    SUPPORTED_MODES,
    get_parser_type,
    set_parser_type,
    SUPPORTED_PARSERS,
    send_udp_command,
    send_all_files,
    send_cmd_list
)

from another_sender.menu_utils import (
    ascii_header,
    clear_screen,
    print_current_config,
    change_command_folder,
    change_comm_mode,
    change_parser_type,
    prompt_for_delay
)

def prompt_for_ip_port():
    """Prompt user for a new IP and port."""
    udp_ip = input("Enter UDP target IP address: ").strip()
    udp_port = int(input("Enter UDP target port: ").strip())
    return udp_ip, udp_port

def prompt_for_config():
    """Prompt user for IP/port or use saved configuration."""
    config = load_config()
    delay = load_delay()

    if "udp_ip" in config and "udp_port" in config:
        print(ascii_header)
        print(f"Loaded saved configuration: {config['udp_ip']}:{config['udp_port']}")
        use_saved = input("Use saved configuration? (Y/N): ").strip().lower()
        if use_saved == 'y':
            udp_ip = config['udp_ip']
            udp_port = config['udp_port']
        else:
            udp_ip, udp_port = prompt_for_ip_port()
            save_config(udp_ip, udp_port)
    else:
        udp_ip, udp_port = prompt_for_ip_port()
        save_config(udp_ip, udp_port)

    return udp_ip, udp_port, delay

def main_menu(udp_ip, udp_port, delay):
    while True:
        clear_screen()
        mode = get_mode()
        parser = get_parser_type()
        folder = get_active_folder()

        print_current_config(__version__, mode, parser, delay, folder)

        files = list_files()
        if not files:
            print("No files found.")
        else:
            for idx, file in enumerate(files, 1):
                print(f"{idx}. {file}")

        print("\n---")
        print("0. Refresh file list")
        print("A. Send all files")
        print("T. Change time delay")
        print("C. Change command folder")
        print("M. Change communication mode")
        print("P. Change parser type")
        print("Q. Quit")

        choice = input("\nSelect a file number to send or choose an option: ").strip().lower()

        if choice == 'q':
            break
        elif choice == '0':
            continue
        elif choice == 'a':
            if mode == "UDP":
                send_all_files(udp_ip, udp_port, delay)
            else:
                print(f"\n❌ Sending all files not yet implemented for mode: {mode}")
                input("Press Enter to continue...")
        elif choice == 't':
            delay = prompt_for_delay(delay, save_delay)
        elif choice == 'c':
            change_command_folder(list_subfolders, set_command_subfolder)
        elif choice == 'm':
            change_comm_mode(get_mode, set_mode, SUPPORTED_MODES)
        elif choice == 'p':
            change_parser_type(get_parser_type, set_parser_type, SUPPORTED_PARSERS)
        else:
            try:
                file_idx = int(choice) - 1
                if 0 <= file_idx < len(files):
                    file_name = files[file_idx]
                    if mode == "UDP":
                        if file_name.upper().startswith("CMD_"):
                            send_cmd_list(file_name, udp_ip, udp_port, delay)
                        else:
                            send_udp_command(file_name, udp_ip, udp_port, delay)
                    else:
                        print(f"\n❌ Sending files not yet implemented for mode: {mode}")
                else:
                    print("Invalid selection. Please choose a valid number.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter a valid number or option.")

        input("\nPress Enter to continue...")

def main():
    parser = argparse.ArgumentParser(description="another-sender CLI tool")
    parser.add_argument("--version", action="store_true", help="Show the version and exit")
    args = parser.parse_args()

    if args.version:
        print(f"another-sender version {__version__}")
        sys.exit(0)

    udp_ip, udp_port, delay = prompt_for_config()
    set_command_subfolder(load_command_subfolder(), persist=False)
    main_menu(udp_ip, udp_port, delay)

if __name__ == "__main__":
    main()
