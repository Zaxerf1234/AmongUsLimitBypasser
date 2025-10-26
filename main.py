from colorama import *
import logging
import struct
import time
import server
import base64
import pyfiglet
def uint(val): # Wrote a short function because I am too lazy to write < 0 check every time
    try:
        intval = int(val)
        if intval < 0:
            raise ValueError(f"invalid literal for uint() with base 10: '{val}'")
        return intval
    except ValueError:
        raise ValueError(f"invalid literal for uint() with base 10: '{val}'")

init()

VERSION = "1.2.0"

# Core settings
reference_hex = "0a8400000100000f00010000000000803f0000803f0000c03f000034420101020100000002010f00000078000000000f0101000000090500000003000000191402000000020000140a0400000003000028140003000000020000190f080000000200000f0009000000020000191e0a0000000300001919020c000000010000031200000001000014"
# Pitch dark
hide_n_seek_ref_hex = "094200000200000a00010000030000803f9a99193fcdcccc3e0101020001000000000048433333b33e0000803e0001000048429a99993f0100ffffffff0000c0400000404000"
maps = { # Turns out bytes before 13th byte are some sort of metadata or version markers
    "skeld": {"id": 0},
    "mira": {"id": 1},
    "polus": {"id": 2},
    "eht dleks": {"id": 3}, # Changing your date to the first of April also works
    "airship": {"id": 4},
    "fungle": {"id": 5}
}

# ------------------ HEX INDEXES AND DATA ------------------

normal_data = { # Offsets for basic settings in the hex
    "map": {
        "byte1": 12, "byte2": None, "type": "map",
        "prompt": f"{Fore.WHITE}Enter map name (Skeld, Mira, Polus, ehT dlekS, Airship, Fungle) or exit to return: {Fore.YELLOW}",
        "error_prompt": f"{Fore.RED}ERROR - Invalid map name!{Fore.WHITE}"
    },
    "impostors": {
        "byte1": 36, "byte2": None, "type": "uint",
        "prompt": f"{Fore.WHITE}Enter impostors count (uint, max 255, note: setting this value to more than 3 or 0 will only work in local lobbies) or exit to return: {Fore.YELLOW}",
        "error_prompt": f"{Fore.RED}ERROR - Invalid number of impostors! Must be a positive non-floating number (uint) between 1 and 3.{Fore.WHITE}"
    },
    "kill_cooldown": {
        "byte1": 25, "byte2": 29, "type": "float",
        "prompt": f"{Fore.WHITE}Enter kill cooldown (float, note: impostors sometimes cannot kill if kill cooldown is set to 0) or exit to return: {Fore.YELLOW}",
        "error_prompt": f"{Fore.RED}ERROR - Invalid kill cooldown! Must be a floating number (float).{Fore.WHITE}"
    },
    "impostor_vision": {
        "byte1": 21, "byte2": 25, "type": "float",
        "prompt": f"{Fore.WHITE}Enter impostor vision (float) or exit to return: {Fore.YELLOW}",
        "error_prompt": f"{Fore.RED}ERROR - Invalid impostor vision! Must be a floating number (float).{Fore.WHITE}"
    },
    "player_speed": {
        "byte1": 13, "byte2": 17, "type": "float",
        "prompt": f"{Fore.WHITE}Enter player speed (float, note: setting this value to more than 3 or less than 0 will only work in local lobbies, public lobby will most likely kick you from the room) or exit to return: {Fore.YELLOW}",
        "error_prompt": f"{Fore.RED}ERROR - Invalid player speed! Must be a floating number (float).{Fore.WHITE}"
    },
    "crewmate_vision": {
        "byte1": 17, "byte2": 21, "type": "float",
        "prompt": f"{Fore.WHITE}Enter crewmate vision (float) or exit to return: {Fore.YELLOW}",
        "error_prompt": f"{Fore.RED}ERROR - Invalid crewmate vision! Must be a floating number (float).{Fore.WHITE}"
    },
    "emergency_meetings": {
        "byte1": 32, "byte2": None, "type": "uint",
        "prompt": f"{Fore.WHITE}Enter emergency meetings count (uint, max 255) or exit to return: {Fore.YELLOW}",
        "error_prompt": f"{Fore.RED}ERROR - Invalid emergency meetings count! Must be a positive non-floating number (uint).{Fore.WHITE}"
    },
    "emergency_cooldown": {
        "byte1": 47, "byte2": None, "type": "uint",
        "prompt": f"{Fore.WHITE}Enter emergency cooldown (uint, max 255) or exit to return: {Fore.YELLOW}",
        "error_prompt": f"{Fore.RED}ERROR - Invalid emergency cooldown! Must be a positive non-floating number (uint).{Fore.WHITE}"
    },
    "discussion_time": {
        "byte1": 38, "byte2": 42, "type": "int",
        "prompt": f"{Fore.WHITE}Enter discussion time (int, note: setting this value to 0 or to a negative number will skip the discussion phase) or exit to return: {Fore.YELLOW}",
        "error_prompt": f"{Fore.RED}ERROR - Invalid discussion time! Must be a non-floating number (int).{Fore.WHITE}"
    },
    "voting_time": {
        "byte1": 42, "byte2": 46, "type": "int",
        "prompt": f"{Fore.WHITE}Enter voting time (int, note: setting this value to 0 or to a negative number will make the voting infinite (it will only end after everyone votes)) or exit to return: {Fore.YELLOW}",
        "error_prompt": f"{Fore.RED}ERROR - Invalid voting time! Must be a non-floating number (int).{Fore.WHITE}"
    },
    "common_tasks": {
        "byte1": 29, "byte2": None, "type": "uint",
        "prompt": f"{Fore.WHITE}Enter common tasks count (uint, max 255, note: setting this value to more than the number of total common tasks on the map will result in completing the same task several times) or exit to return: {Fore.YELLOW}",
        "error_prompt": f"{Fore.RED}ERROR - Invalid common tasks count! Must be a positive non-floating number (uint).{Fore.WHITE}"
    },
    "long_tasks": {
        "byte1": 30, "byte2": None, "type": "uint",
        "prompt": f"{Fore.WHITE}Enter long tasks count (uint, max 255, note: setting this value to more than the number of total long tasks on the map will result in completing the same task several times) or exit to return: {Fore.YELLOW}",
        "error_prompt": f"{Fore.RED}ERROR - Invalid long tasks count! Must be a positive non-floating number (uint).{Fore.WHITE}"
    },
    "short_tasks": {
        "byte1": 31, "byte2": None, "type": "uint",
        "prompt": f"{Fore.WHITE}Enter short tasks count (uint, max 255, note: setting this value to more than the number of total short tasks on the map will result in completing the same task several times) or exit to return: {Fore.YELLOW}",
        "error_prompt": f"{Fore.RED}ERROR - Invalid short tasks count! Must be a positive non-floating number (uint).{Fore.WHITE}"
    },
}

hns_data = { # Offsets for hide n seek settings in the hex
    "map": {
        "byte1": 12, "byte2": None, "type": "map",
        "prompt": f"{Fore.WHITE}Enter map name (Skeld, Mira, Polus, ehT dlekS, Airship, Fungle) or exit to return: {Fore.YELLOW}",
        "error_prompt": f"{Fore.RED}ERROR - Invalid map name!{Fore.WHITE}"
    },
    "player_speed": {
        "byte1": 13, "byte2": 17, "type": "float",
        "prompt": f"{Fore.WHITE}Enter player speed (float, note: setting this value to more than 3 or less than 0 will only work in local lobbies) or exit to return: {Fore.YELLOW}",
        "error_prompt": f"{Fore.RED}ERROR - Invalid player speed! Must be a floating number (float).{Fore.WHITE}"
    },
    "hiding_time": {
        "byte1": 35, "byte2": 39, "type": "midbigfloat",
        "prompt": f"{Fore.WHITE}Enter hiding time (float, note: may be incorrect due to among us rounding) or exit to return: {Fore.YELLOW}",
        "error_prompt": f"{Fore.RED}ERROR - Invalid hiding time! Must be a floating number (float).{Fore.WHITE}"
    },
    "crewmate_vision": {
        "byte1": 17, "byte2": 21, "type": "float",
        "prompt": f"{Fore.WHITE}Enter crewmate vision (float) or exit to return: {Fore.YELLOW}",
        "error_prompt": f"{Fore.RED}ERROR - Invalid crewmate vision! Must be a floating number (float).{Fore.WHITE}"
    },
    "vent_uses": {
        "byte1": 29, "byte2": None, "type": "uint",
        "prompt": f"{Fore.WHITE}Enter vent uses count (uint, max 255) or exit to return: {Fore.YELLOW}",
        "error_prompt": f"{Fore.RED}ERROR - Invalid vent uses count! Must be a positive non-floating number (uint).{Fore.WHITE}"
    },
    "max_vent_time": {
        "byte1": 67, "byte2": 71, "type": "midbigfloat",
        "prompt": f"{Fore.WHITE}Enter max time in vent (float, note: may be incorrect due to among us rounding) or exit to return: {Fore.YELLOW}",
        "error_prompt": f"{Fore.RED}ERROR - Invalid max time in vent! Must be a floating number (float).{Fore.WHITE}"
    },
    "crewmate_flashlight_size": {
        "byte1": 37, "byte2": 41, "type": "float",
        "prompt": f"{Fore.WHITE}Enter crewmate flashlight size (float) or exit to return: {Fore.YELLOW}",
        "error_prompt": f"{Fore.RED}ERROR - Invalid crewmate flashlight size! Must be a floating number (float).{Fore.WHITE}"
    },
    "impostor_flashlight_size": {
        "byte1": 41, "byte2": 45, "type": "float",
        "prompt": f"{Fore.WHITE}Enter impostor flashlight size (float) or exit to return: {Fore.YELLOW}",
        "error_prompt": f"{Fore.RED}ERROR - Invalid impostor flashlight size! Must be a floating number (float).{Fore.WHITE}"
    },
    "impostor_vision": {
        "byte1": 21, "byte2": 25, "type": "float",
        "prompt": f"{Fore.WHITE}Enter impostor vision (float) or exit to return: {Fore.YELLOW}",
        "error_prompt": f"{Fore.RED}ERROR - Invalid impostor vision! Must be a floating number (float).{Fore.WHITE}"
    },
    "final_time": {
        "byte1": 47, "byte2": 51, "type": "float",
        "prompt": f"{Fore.WHITE}Enter final hide time (float, note: may be incorrect due to among us rounding) or exit to return: {Fore.YELLOW}",
        "error_prompt": f"{Fore.RED}ERROR - Invalid final hide time! Must be a floating number (float).{Fore.WHITE}"
    },
    "final_impostor_speed": {
        "byte1": 51, "byte2": 55, "type": "float",
        "prompt": f"{Fore.WHITE}Enter final hide impostor speed (float) or exit to return: {Fore.YELLOW}",
        "error_prompt": f"{Fore.RED}ERROR - Invalid final hide impostor speed! Must be a floating number (float).{Fore.WHITE}"
    },
    "ping_interval": {
        "byte1": 63, "byte2": 67, "type": "midbigfloat",
        "prompt": f"{Fore.WHITE}Enter ping interval (float) or exit to return: {Fore.YELLOW}",
        "error_prompt": f"{Fore.RED}ERROR - Invalid ping interval! Must be a floating number (float).{Fore.WHITE}"
    },
    "common_tasks": {
        "byte1": 25, "byte2": None, "type": "uint",
        "prompt": f"{Fore.WHITE}Enter common tasks count (uint, max 255) or exit to return: {Fore.YELLOW}",
        "error_prompt": f"{Fore.RED}ERROR - Invalid common tasks count! Must be a positive non-floating number (uint).{Fore.WHITE}"
    },
    "long_tasks": {
        "byte1": 26, "byte2": None, "type": "uint",
        "prompt": f"{Fore.WHITE}Enter long tasks count (uint, max 255) or exit to return: {Fore.YELLOW}",
        "error_prompt": f"{Fore.RED}ERROR - Invalid long tasks count! Must be a positive non-floating number (uint).{Fore.WHITE}"
    },
    "short_tasks": {
        "byte1": 27, "byte2": None, "type": "uint",
        "prompt": f"{Fore.WHITE}Enter short tasks count (uint, max 255) or exit to return: {Fore.YELLOW}",
        "error_prompt": f"{Fore.RED}ERROR - Invalid short tasks count! Must be a positive non-floating number (uint).{Fore.WHITE}"
    }
}

role_bytes = { # Offsets for role settings in the hex
    "Shapeshifter": {
        "count": 56,
        "chance": 57,
        "shapeshift_cooldown": 62,
        "shapeshift_duration": 63,
    },
    "Scientist": {
        "count": 66,
        "chance": 67,
        "vitals_display_cooldown": 71,
        "battery_duration": 72,
    },
    "Guardian Angel": {
        "count": 75,
        "chance": 76,
        "protect_cooldown": 80,
        "protection_duration": 81,
    },
    "Engineer": {
        "count": 85,
        "chance": 86,
        "vent_use_cooldown": 90,
        "max_time_in_vents": 91,
    },
    "Noisemaker": {
        "count": 94,
        "chance": 95,
        "alert_duration": 99,
    },
    "Phantom": {
        "count": 103,
        "chance": 104,
        "vanish_cooldown": 108,
        "vanish_duration": 109,
    },
    "Tracker": {
        "count": 112,
        "chance": 113,
        "tracking_cooldown": 117,
        "tracking_duration": 118,
        "tracking_delay": 119,
    },
    "Detective": {
        "count": 122,
        "chance": 123,
        "suspects_per_case": 127,
    },
    "Viper": {
        "count": 130,
        "chance": 131,
        "dissolve_time": 135,
    }
}

normal_hex_len = 272
hns_hex_len = 142
second_hns_hex_len = 140

# ------------------ FUNCTIONS AND CODE ------------------

def set_data(hex_data, prompt, error_prompt, type, byte1, byte2):
    if type == "map":
        while True:
            try:
                map = input(f"{Fore.WHITE}Enter map name (Skeld, Mira, Polus, ehT dlekS, Airship, Fungle) or exit to return: {Fore.YELLOW}")
                if map.lower() == "exit":
                    return None
                if map.lower() == "eht dleks":
                    print(f"{Fore.YELLOW}WARN - Skeld backwards (ehT dlekS) may not work in normal game or online lobby!{Fore.WHITE}")
                if map.lower() not in maps.keys():
                    print(f"{Fore.RED}ERROR - Invalid map name!{Fore.WHITE}")
                    continue
                hex_data[byte1] = maps[map.lower()]["id"] # I hate maps
                return "Success"
            except Exception as e:
                print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
                continue
    elif type == "uint":
        while True:
            try:
                val = input(f"{Fore.WHITE}{prompt}{Fore.YELLOW}")
                if val == "exit":
                    return None
                try:
                    val = uint(val)
                except:
                    print(f"{Fore.RED}{error_prompt}{Fore.WHITE}")
                    continue
                hex_data[byte1] = val
                return "Success"
            except Exception as e:
                print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
                continue
    elif type == "int":
        while True:
            try:
                val = input(f"{Fore.WHITE}{prompt}{Fore.YELLOW}")
                if val == "exit":
                    return None
                try:
                    val = int(val)
                except:
                    print(f"{Fore.RED}{error_prompt}{Fore.WHITE}")
                    continue
                hex_data[byte1:byte2] = struct.pack('<i', val)
                return "Success"
            except Exception as e:
                print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
                continue
    elif type == "float":
        while True:
            try:
                val = input(f"{Fore.WHITE}{prompt}{Fore.YELLOW}")
                if val == "exit":
                    return None
                try:
                    val = float(val)
                except:
                    print(f"{Fore.RED}ERROR - Invalid kill cooldown! Must be a floating number (float).{Fore.WHITE}")
                    continue
                hex_data[byte1:byte2] = struct.pack('<f', val)
                return "Success"
            except Exception as e:
                print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
                continue
    elif type == "midbigfloat":
        while True:
            try:
                val = input(f"{Fore.WHITE}{prompt}{Fore.YELLOW}")
                if val == "exit":
                    return None
                try:
                    val = float(val)
                except:
                    print(f"{Fore.RED}{error_prompt}{Fore.WHITE}")
                    continue
                hex_data[byte1:byte2] = struct.pack('>f', val)[1::-1] + struct.pack('>f', val)[3:1:-1]
                return "Success"
            except Exception as e:
                print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
                continue
        

def process_data(string, mode):
    if mode == "encode":
        if not string: # If no argument
            string = input(f"{Fore.WHITE}Modified hex: {Fore.YELLOW}")
            try:
                bytes_data = bytes.fromhex(string)
            except ValueError:
                print(f"{Fore.RED}ERROR - Invalid hex string!{Fore.WHITE}")
                return

            if len(string) == normal_hex_len:
                print(f"{Fore.GREEN}{normal_hex_len} characters - OK for normal{Fore.WHITE}")
                print(f"Output base64:{Fore.BLUE}", base64.b64encode(bytes_data).decode(), Fore.WHITE)
            elif len(string) == hns_hex_len or len(string) == second_hns_hex_len:
                print(f"{Fore.GREEN}{len(string)} characters - OK for hide n seek{Fore.WHITE}")
                print(f"Output base64:{Fore.BLUE}", base64.b64encode(bytes_data).decode(), Fore.WHITE)
            else:
                print(f"{Fore.RED}ERROR - {len(string)} characters, the game may not load!{Fore.WHITE}")
                print(f"Output base64:{Fore.BLUE}", base64.b64encode(bytes_data).decode(), Fore.WHITE)
        else: # If some argument
            try:
                bytes_data = bytes.fromhex(string)
            except ValueError:
                return f"{Fore.RED}ERROR - Invalid hex string!{Fore.WHITE}"
            
            if len(string) == normal_hex_len:
                print(f"{Fore.GREEN}{normal_hex_len} characters - OK for normal{Fore.WHITE}")
                return base64.b64encode(bytes_data).decode()
            elif len(string) == hns_hex_len or len(string) == second_hns_hex_len:
                print(f"{Fore.GREEN}{len(string)} characters - OK for hide n seek{Fore.WHITE}")
                return base64.b64encode(bytes_data).decode()
            else:
                print(f"{Fore.RED}ERROR - {len(string)} characters, the game may not load!{Fore.WHITE}")
                return base64.b64encode(bytes_data).decode()
    elif mode == "decode":
        if not string:
            string = input(f"{Fore.WHITE}Base64 string: {Fore.YELLOW}")
            try:
                bytes_data = base64.b64decode(string)
            except (ValueError, base64.binascii.Error):
                print(f"{Fore.RED}ERROR - Invalid Base64 string!{Fore.WHITE}")
                return 

            hex_output = bytes_data.hex()
            print(f"Output hex: {Fore.BLUE}{hex_output}{Fore.WHITE}")
        else:
            try:
                bytes_data = base64.b64decode(string)
            except (ValueError, base64.binascii.Error):
                return f"{Fore.RED}ERROR - Invalid Base64 string!{Fore.WHITE}"

            hex_output = bytes_data.hex()
            return hex_output


def modify_normal_among_us_hex(reference_hex):
    hex_data = bytearray.fromhex(reference_hex)

    # Basic settings
    for key, info in normal_data.items():
        res = set_data(hex_data, info["prompt"], info["error_prompt"], info["type"], info["byte1"], info["byte2"])
        if res is None:
            return None

    # Roles
    while True:
        roles = input(f"{Fore.WHITE}Do you want to customize roles? (true/false) {Fore.YELLOW}")
        if roles == "exit":
            return None
        if roles.lower() == "true":
            break
        elif roles.lower() == "false":
            return hex_data.hex()
        else:
            print(f"{Fore.RED}ERROR - Invalid input! Must be 'true' or 'false'.{Fore.WHITE}")
            continue

    logging.getLogger('werkzeug').disabled = True
    while True:
        print(f"{Fore.MAGENTA}Please fill out the form in another window.{Fore.WHITE}")
        roles_json = server.run("window") # run the server webview in window mode

        if roles_json is None:
            print(f"{Fore.RED}ERROR - Roles customization window was closed without submitting data or something went wrong. Restarting in 3 seconds...{Fore.WHITE}")
            time.sleep(3)
            continue
        else:
            server.submitted_data = None
            break

    for role, fields in role_bytes.items():
        for field, offset in fields.items():
            hex_data[offset] = roles_json[role][field]

    return hex_data.hex()


def modify_hide_n_seek_among_us_hex(reference_hex):
    hex_data = bytearray.fromhex(reference_hex)

    # Basic settings
    for key, info in hns_data.items():
        res = set_data(hex_data, info["prompt"], info["error_prompt"], info["type"], info["byte1"], info["byte2"])
        if res is None:
            return None

    return hex_data.hex()

def main():
    while True:
        print()
        print()
        print(f"{Fore.YELLOW}1. Modify normal Among Us hex{Fore.WHITE}")
        print(f"{Fore.YELLOW}2. Modify Hide n Seek Among Us hex{Fore.WHITE}")
        print(f"{Fore.YELLOW}3. Encode modified hex to Base64{Fore.WHITE}")
        print(f"{Fore.YELLOW}4. Decode Base64 to hex{Fore.WHITE}")
        print(f"{Fore.YELLOW}5. Exit{Fore.WHITE}")
        choice = input(f"{Fore.WHITE}Choose an option: {Fore.YELLOW}")

        if choice.lower() == "1":
            hex_output = modify_normal_among_us_hex(reference_hex)
            if hex_output is None: continue
            print(f"Base64 output: {process_data(hex_output, "encode")} \nHex output (advanced): {hex_output}")
        elif choice.lower() == "2":
            hex_output = modify_hide_n_seek_among_us_hex(hide_n_seek_ref_hex)
            if hex_output is None: continue
            print(f"Base64 output: {process_data(hex_output, "encode")} \nHex output (advanced): {hex_output}")
        elif choice.lower() == "3":
            process_data(None, "encode")
        elif choice.lower() == "4":
            process_data(None, "decode")
        elif choice.lower() == "5":
            quit()
        else:
            print(f"{Fore.RED}Invalid option!{Fore.WHITE}")

if __name__ == "__main__":
    print(pyfiglet.figlet_format("Among Us Limit Bypasser", font="modular"))
    print("Copyright (C) 2025 Zaxerf1234")
    print("Full license: https://github.com/Zaxerf1234/AmongUsLimitBypasser/blob/main/LICENSE")
    print(f"Made with love by Zaxerf1234. Version {VERSION} (source code: https://github.com/Zaxerf1234/AmongUsLimitBypasser)")
    main()
