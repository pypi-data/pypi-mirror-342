import os
import sys
import argparse

from another_sender import __version__
from another_sender.udp_utils import (
    load_config,
    save_config,
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

from another_sender.meta_utils import load_delay, save_delay

from another_sender.menu_utils import (
    ascii_header,
    clear_screen,
    print_current_config,
    change_command_folder,
    change_parser_type,
    prompt_for_delay
)

from another_sender.history_utils import (
    add_to_history,
    display_history,
    get_history_entry
)

def prompt_for_ip_port():
    udp_ip = input("Enter UDP target IP address: ").strip()
    udp_port = int(input("Enter UDP target port: ").strip())
    return udp_ip, udp_port

def main_menu(udp_ip, udp_port, delay):
    config = load_config()

    while True:
        clear_screen()
        mode = get_mode()
        parser = get_parser_type()
        folder = get_active_folder()

        connection_info = {}
        if mode == "UDP":
            connection_info = {
                "Target IP": config.get("udp_ip", "Not Set"),
                "Target Port": config.get("udp_port", "Not Set")
            }
        elif mode == "SPI":
            connection_info = {
                "SPI Bus": config.get("spi_bus", "Not Set"),
                "SPI Device": config.get("spi_device", "Not Set")
            }

        print_current_config(__version__, mode, parser, delay, folder, connection_info)

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
        print("H. View command history")
        print("R. Resend from history")
        print("V. Start receive mode")
        print("Q. Quit")

        choice = input("\nSelect a file number to send or choose an option: ").strip().lower()

        if choice == 'q':
            break
        elif choice == '0':
            continue
        elif choice == 'a':
            if mode == "UDP":
                send_all_files(config.get("udp_ip"), config.get("udp_port"), delay)
            else:
                print(f"\n❌ Sending all files not yet implemented for mode: {mode}")
                input("Press Enter to continue...")
        elif choice == 't':
            delay = prompt_for_delay(delay, save_delay)
        elif choice == 'c':
            change_command_folder(list_subfolders, set_command_subfolder)
        elif choice == 'm':
            old_mode = get_mode()
            print(f"Current mode: {old_mode}")
            print("Available communication modes:\n")
            for i, mode_name in enumerate(SUPPORTED_MODES, 1):
                print(f"  {i}. {mode_name}")
            try:
                selection = int(input("\nSelect a new mode by number: ").strip())
                if 1 <= selection <= len(SUPPORTED_MODES):
                    new_mode = SUPPORTED_MODES[selection - 1]
                    set_mode(new_mode)

                    if new_mode == "UDP" and old_mode != "UDP":
                        clear_screen()
                        print(ascii_header)
                        udp_ip = config.get("udp_ip", "Not Set")
                        udp_port = config.get("udp_port", "Not Set")
                        print(f"\n🔌 Current UDP Configuration: {udp_ip}:{udp_port}")
                        change = input("Would you like to change it? (Y/N): ").strip().lower()
                        if change == 'y':
                            udp_ip, udp_port = prompt_for_ip_port()
                            config["udp_ip"] = udp_ip
                            config["udp_port"] = udp_port
                            save_config(udp_ip, udp_port)
                            print("✅ Updated UDP configuration.")
                        else:
                            print("ℹ️  Keeping existing UDP configuration.")
                else:
                    print("❌ Invalid selection.")
            except ValueError:
                print("❌ Please enter a valid number.")
        elif choice == 'p':
            change_parser_type(get_parser_type, set_parser_type, SUPPORTED_PARSERS)
        elif choice == 'h':
            clear_screen()
            display_history()
        elif choice == 'r':
            display_history()
            try:
                index = int(input("\nEnter history item number to resend: ").strip()) - 1
                entry = get_history_entry(index)
                if not entry:
                    print("❌ Invalid history selection.")
                else:
                    filename = entry["filename"]
                    mode = entry["mode"]
                    conn = entry.get("connection", {})

                    if mode == "UDP":
                        udp_ip = conn.get("ip")
                        udp_port = conn.get("port")
                        if udp_ip and udp_port:
                            if filename.upper().startswith("CMD_"):
                                send_cmd_list(filename, udp_ip, udp_port, delay)
                            else:
                                send_udp_command(filename, udp_ip, udp_port, delay)
                            add_to_history(filename, "UDP", {"ip": udp_ip, "port": udp_port})
                            print("✅ Resent from history.")
                        else:
                            print("❌ Incomplete UDP configuration.")
                    else:
                        print(f"❌ Resend not implemented for mode: {mode}")
            except (ValueError, IndexError):
                print("❌ Invalid input.")
        elif choice == 'v':
            try:
                from another_sender.udp_utils import start_receive_mode
                import socket

                def list_local_ips():
                    hostname = socket.gethostname()
                    try:
                        ips = socket.gethostbyname_ex(hostname)[2]
                        ips = list({ip for ip in ips if '.' in ip})
                        ips.sort()
                    except Exception:
                        ips = []
                    return ips

                interfaces = list_local_ips()
                print("\n📡 Select interface to listen on:")
                for i, ip in enumerate(interfaces, 1):
                    print(f"  {i}. {ip}")
                print("  0. All interfaces (0.0.0.0)")

                selection = input("\nEnter number: ").strip()
                if selection == "0" or not selection:
                    local_ip = "0.0.0.0"
                else:
                    index = int(selection) - 1
                    local_ip = interfaces[index] if 0 <= index < len(interfaces) else "0.0.0.0"

                local_port = config.get("udp_port", 5005)
                start_receive_mode(local_ip, local_port)

            except Exception as e:
                print(f"❌ Failed to start receive mode: {e}")
        else:
            try:
                file_idx = int(choice) - 1
                if 0 <= file_idx < len(files):
                    file_name = files[file_idx]
                    if mode == "UDP":
                        udp_ip = config.get("udp_ip")
                        udp_port = config.get("udp_port")
                        if udp_ip and udp_port:
                            if file_name.upper().startswith("CMD_"):
                                send_cmd_list(file_name, udp_ip, udp_port, delay)
                            else:
                                send_udp_command(file_name, udp_ip, udp_port, delay)
                            add_to_history(file_name, "UDP", {"ip": udp_ip, "port": udp_port})
                        else:
                            print("❌ UDP IP/Port not configured. Switch to UDP mode to set them.")
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

    delay = load_delay()
    set_command_subfolder(load_command_subfolder(), persist=False)
    config = load_config()
    main_menu(config.get("udp_ip"), config.get("udp_port"), delay)

if __name__ == "__main__":
    main()
