# menu_utils.py

import os

# --- UI Banner ---
ascii_header = """
******************************************
*   📂 ➡️  📡 Command File Sender 📦   *
******************************************
"""

def clear_screen():
    """Clear terminal and print banner."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(ascii_header)

def print_current_config(version, mode, parser, delay, folder, connection_info=None):
    print(f"🛠️  Version: {version}")
    print(f"📡 Mode: {mode}")

    if connection_info:
        print("🔌 Connection:")
        for key, value in connection_info.items():
            print(f"   {key}: {value}")

    print(f"🧩 Parser: {parser}")
    print(f"⏱️  Delay: {delay} sec")
    print(f"📂 Folder: {folder}")
    print("---")


def change_command_folder(list_subfolders, set_command_subfolder):
    """Allow user to select a subfolder inside 'commands/'."""
    subfolders = list_subfolders()
    if not subfolders:
        print("No subfolders found inside 'commands/'.")
        input("Press Enter to return to the menu...")
        return

    print("\nAvailable command folders:")
    for idx, folder in enumerate(subfolders, 1):
        print(f"{idx}. {folder}")
    print("B. Back")

    while True:
        choice = input("Select a folder by number or B to go back: ").strip().lower()
        if choice == 'b':
            return
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(subfolders):
                selected = subfolders[idx]
                set_command_subfolder(selected, persist=True)
                print(f"\n✅ Switched to: {selected}")
                return
            else:
                print("Invalid index.")
        except ValueError:
            print("Invalid input.")

def change_comm_mode(get_mode, set_mode, SUPPORTED_MODES):
    """Allow user to switch communication mode."""
    print("\nAvailable communication modes:")
    for idx, mode in enumerate(SUPPORTED_MODES, 1):
        print(f"{idx}. {mode}")
    print("B. Back")

    while True:
        choice = input("Select a mode by number or B to go back: ").strip().lower()
        if choice == 'b':
            return
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(SUPPORTED_MODES):
                selected = SUPPORTED_MODES[idx]
                set_mode(selected)
                print(f"\n✅ Communication mode set to: {selected}")
                return
            else:
                print("Invalid index.")
        except ValueError:
            print("Invalid input.")

def change_parser_type(get_parser_type, set_parser_type, SUPPORTED_PARSERS):
    """Allow user to switch parser type."""
    print("\nAvailable parser types:")
    for idx, parser in enumerate(SUPPORTED_PARSERS, 1):
        print(f"{idx}. {parser}")
    print("B. Back")

    while True:
        choice = input("Select a parser by number or B to go back: ").strip().lower()
        if choice == 'b':
            return
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(SUPPORTED_PARSERS):
                selected = SUPPORTED_PARSERS[idx]
                set_parser_type(selected)
                print(f"\n✅ Parser type set to: {selected}")
                return
            else:
                print("Invalid index.")
        except ValueError:
            print("Invalid input.")

def prompt_for_delay(current_delay, save_delay):
    """Prompt user for a new delay value in seconds."""
    try:
        new_delay = float(input("Enter new delay in seconds: "))
        if new_delay < 0:
            print("Delay cannot be negative. Keeping previous value.")
            return current_delay
        save_delay(new_delay)
        return new_delay
    except ValueError:
        print("Invalid input. Delay must be a number.")
        return current_delay
