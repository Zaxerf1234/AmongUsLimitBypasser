from colorama import *
import struct
import base64
import pyfiglet
def uint(val): # Wrote a short function becuase I am too lazy to write < 0 check every time
    try:
        intval = int(val)
        if intval < 0:
            raise ValueError(f"invalid literal for uint() with base 10: '{val}'")
        return intval
    except ValueError:
        raise ValueError(f"invalid literal for uint() with base 10: '{val}'")

init()

VERSION = "1.1.0"

# Core settings
reference_hex = "097400000100000f00010000000000803f0000803f0000c03f000034420101020100000001010f00000078000000000001010000000705000000030000000a1e020000000200000f05040000000300003c0a00030000000200001e0f080000000200000a01090000000200000f1e0a0000000300000f1e01"
# Pitch dark
hide_n_seek_ref_hex = "094200000200000a00010000030000803f9a99193fcdcccc3e0101020001000000000048433333b33e0000803e0001000048429a99993f0100ffffffff0000c0400000404000"
maps = { # Didn't figure out how to edit map bytes, so wrote a dict for every map hex, they may change after among us update
    "skeld": {"normal": "640f0001000000", "id": 0},
    "mira": {"normal": "000a0001000001", "id": 1},
    "polus": {"normal": "000f0001020002", "id": 2},
    "eht dleks": {"normal": "00000000000003", "id": 3}, # Only can find it in hide n seek, not in normal among us
    "airship": {"normal": "000f0001020004", "id": 4},
    "fungle": {"normal": "000f0001020005", "id": 5}
}

def encode_base64(hex_str):
    if not hex_str: # If no argument
        hex_str = input(f"{Fore.WHITE}Modified hex: {Fore.YELLOW}")
        try:
            bytes_data = bytes.fromhex(hex_str)
        except ValueError:
            print(f"{Fore.RED}ERROR - Invalid hex string!{Fore.WHITE}")
            return

        if len(hex_str) == 240:
            print(f"{Fore.GREEN}240 characters - OK for normal{Fore.WHITE}")
            print(f"Output base64:{Fore.BLUE}", base64.b64encode(bytes_data).decode(), Fore.WHITE)
        elif len(hex_str) == 120 or len(hex_str) == 122:
            print(f"{Fore.GREEN}{len(hex_str)} characters - OK for hide n seek{Fore.WHITE}")
            print(f"Output base64:{Fore.BLUE}", base64.b64encode(bytes_data).decode(), Fore.WHITE)
        else:
            print(f"{Fore.RED}ERROR - {len(hex_str)} characters, the game may not load!{Fore.WHITE}")
            print(f"Output base64:{Fore.BLUE}", base64.b64encode(bytes_data).decode(), Fore.WHITE)
    else: # If some argument
        try:
            bytes_data = bytes.fromhex(hex_str)
        except ValueError:
            return f"{Fore.RED}ERROR - Invalid hex string!{Fore.WHITE}"
        
        if len(hex_str) == 240:
            print(f"{Fore.GREEN}240 characters - OK for normal{Fore.WHITE}")
            return base64.b64encode(bytes_data).decode()
        elif len(hex_str) == 140 or len(hex_str) == 142:
            print(f"{Fore.GREEN}{len(hex_str)} characters - OK for hide n seek{Fore.WHITE}")
            return base64.b64encode(bytes_data).decode()
        else:
            print(f"{Fore.RED}ERROR - {len(hex_str)} characters, the game may not load!{Fore.WHITE}")
            return base64.b64encode(bytes_data).decode()

def decode_base64(base64_str):
    if not base64_str:
        base64_str = input(f"{Fore.WHITE}Base64 string: {Fore.YELLOW}")
        try:
            bytes_data = base64.b64decode(base64_str)
        except (ValueError, base64.binascii.Error):
            print(f"{Fore.RED}ERROR - Invalid Base64 string!{Fore.WHITE}")
            return 

        hex_output = bytes_data.hex()
        print(f"Output hex: {Fore.BLUE}{hex_output}{Fore.WHITE}")
    else:
        try:
            bytes_data = base64.b64decode(base64_str)
        except (ValueError, base64.binascii.Error):
            return f"{Fore.RED}ERROR - Invalid Base64 string!{Fore.WHITE}"

        hex_output = bytes_data.hex()
        return hex_output

def modify_normal_among_us_hex(reference_hex):
    hex_data = bytearray.fromhex(reference_hex)
    success_flag = False

    # Map
    while not success_flag:
        try:
            map = input(f"{Fore.WHITE}Enter map name (Skeld, Mira, Polus, ehT dlekS, Airship, Fungle) or exit to return: {Fore.YELLOW}")
            if map.lower() == "exit":
                return None
            if map.lower() == "eht dleks":
                print(f"{Fore.YELLOW}WARN - Skeld backwards (ehT dlekS) may not work in normal game or online lobby!{Fore.WHITE}")
            if map.lower() not in maps.keys():
                print(f"{Fore.RED}ERROR - Invalid map name!{Fore.WHITE}")
                continue
            hex_data[6:13] = struct.pack('>7s', bytes.fromhex(maps[map.lower()]["normal"])) # I hate maps
            success_flag = True
        except Exception as e:
            print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
            continue
    success_flag = False

    # Impostors
    while not success_flag:
        try:
            impostors = input(f"{Fore.WHITE}Enter impostors count (uint, max 255, note: setting this value to more than 3 or 0 will only work in local lobbies)) or exit to return: {Fore.YELLOW}")
            if impostors == "exit":
                return None
            try:
                impostors = uint(impostors)
            except:
                print(f"{Fore.RED}ERROR - Invalid impostors count! Must be a positive non-floating number (uint).{Fore.WHITE}")
                continue
            hex_data[36] = impostors
            success_flag = True
        except Exception as e:
            print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
            continue
    success_flag = False

    # Kill Cooldown
    while not success_flag:
        try:
            kill_cooldown = input(f"{Fore.WHITE}Enter kill cooldown (float, note: impostors sometimes cannot kill if kill cooldown is set to 0) or exit to return: {Fore.YELLOW}")
            if kill_cooldown == "exit":
                return None
            try:
                kill_cooldown = float(kill_cooldown)
            except:
                print(f"{Fore.RED}ERROR - Invalid kill cooldown! Must be a floating number (float).{Fore.WHITE}")
                continue
            hex_data[25:29] = struct.pack('<f', kill_cooldown)
            success_flag = True
        except Exception as e:
            print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
            continue
    success_flag = False

    # Impostor Vision
    while not success_flag:
        try:
            impostor_vision = input(f"{Fore.WHITE}Enter impostor vision (float) or exit to return: {Fore.YELLOW}")
            if impostor_vision == "exit":
                return None
            try:
                impostor_vision = float(impostor_vision)
            except:
                print(f"{Fore.RED}ERROR - Invalid impostor vision! Must be a floating number (float).{Fore.WHITE}")
                continue
            hex_data[21:25] = struct.pack('<f', impostor_vision)
            success_flag = True
        except Exception as e:
            print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
            continue
    success_flag = False

    # Player Speed
    while not success_flag:
        try:
            player_speed = input(f"{Fore.WHITE}Enter player speed (float, note: setting this value to more than 3 or less than 0 will only work in local lobbies, public lobby will most likely kick you from the room) or exit to return: {Fore.YELLOW}")
            if player_speed == "exit":
                return None
            try:
                player_speed = float(player_speed)
            except:
                print(f"{Fore.RED}ERROR - Invalid player speed! Must be a floating number (float).{Fore.WHITE}")
                continue
            hex_data[13:17] = struct.pack('<f', player_speed)
            success_flag = True
        except Exception as e:
            print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
            continue
    success_flag = False

    # Crewmate Vision
    while not success_flag:
        try:
            crewmate_vision = input(f"{Fore.WHITE}Enter crewmate vision (float) or exit to return: {Fore.YELLOW}")
            if crewmate_vision == "exit":
                return None
            try:
                crewmate_vision = float(crewmate_vision)
            except:
                print(f"{Fore.RED}ERROR - Invalid crewmate vision! Must be a floating number (float).{Fore.WHITE}")
                continue
            hex_data[17:21] = struct.pack('<f', crewmate_vision)
            success_flag = True
        except Exception as e:
            print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
            continue
    success_flag = False

    # Emergency Meetings
    while not success_flag:
        try:
            emergency_meetings = input(f"{Fore.WHITE}Enter emergency meetings count (uint, max 255)) or exit to return: {Fore.YELLOW}")
            if emergency_meetings == "exit":
                return None
            try:
                emergency_meetings = uint(emergency_meetings)
            except:
                print(f"{Fore.RED}ERROR - Invalid emergency meetings count! Must be a positive non-floating number (uint).{Fore.WHITE}")
                continue
            hex_data[32] = emergency_meetings
            success_flag = True
        except Exception as e:
            print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
            continue
    success_flag = False

    # Emergency Cooldown
    while not success_flag:
        try:
            emergency_cooldown = input(f"{Fore.WHITE}Enter emergency cooldown (uint, max 255) or exit to return: {Fore.YELLOW}")
            if emergency_cooldown == "exit":
                return None
            try:
                emergency_cooldown = uint(emergency_cooldown)
            except:
                print(f"{Fore.RED}ERROR - Invalid emergency cooldown! Must be a positive non-floating number (uint).{Fore.WHITE}")
                continue
            hex_data[47] = emergency_cooldown
            success_flag = True
        except Exception as e:
            print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
            continue
    success_flag = False

    # Discussion Time
    while not success_flag:
        try:
            discussion_time = input(f"{Fore.WHITE}Enter discussion time (int, note: setting this value to 0 or to a negative number will skip the discussion phase) or exit to return: {Fore.YELLOW}")
            if discussion_time == "exit":
                return None
            try:
                discussion_time = int(discussion_time)
            except:
                print(f"{Fore.RED}ERROR - Invalid discussion time! Must be a non-floating number (int).{Fore.WHITE}")
                continue
            hex_data[38:42] = struct.pack('<i', discussion_time)
            success_flag = True
        except Exception as e:
            print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
            continue
    success_flag = False

    # Voting Time
    while not success_flag:
        try:
            voting_time = input(f"{Fore.WHITE}Enter voting time (int, note: setting this value to 0 or to a negative number will make the voting infinite (it will only end after everyone votes)) or exit to return: {Fore.YELLOW}")
            if voting_time == "exit":
                return None
            try:
                voting_time = int(voting_time)
            except:
                print(f"{Fore.RED}ERROR - Invalid voting time! Must be a non-floating number (int).{Fore.WHITE}")
                continue
            hex_data[42:46] = struct.pack('<i', voting_time)
            success_flag = True
        except Exception as e:
            print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
            continue
    success_flag = False

    # Common Tasks
    while not success_flag:
        try:
            common_tasks = input(f"{Fore.WHITE}Enter common tasks count (uint, max 255, note: settings this value to more than the number of total common tasks on the map will result in completing the same task for several times) or exit to return: {Fore.YELLOW}")
            if common_tasks == "exit":
                return None
            try:
                common_tasks = uint(common_tasks)
            except:
                print(f"{Fore.RED}ERROR - Invalid common tasks count! Must be a positive non-floating number (uint).{Fore.WHITE}")
                continue
            hex_data[29] = common_tasks
            success_flag = True
        except Exception as e:
            print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
            continue
    success_flag = False

    # Long Tasks
    while not success_flag:
        try:
            long_tasks = input(f"{Fore.WHITE}Enter long tasks count (uint, max 255, note: settings this value to more than the number of total long tasks on the map will result in completing the same task for several times) or exit to return: {Fore.YELLOW}")
            if long_tasks == "exit":
                return None
            try:
                long_tasks = uint(long_tasks)
            except:
                print(f"{Fore.RED}ERROR - Invalid long tasks count! Must be a positive non-floating number (uint).{Fore.WHITE}")
                continue
            hex_data[30] = long_tasks
            success_flag = True
        except Exception as e:
            print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
            continue
    success_flag = False

    # Short Tasks
    while not success_flag:
        try:
            short_tasks = input(f"{Fore.WHITE}Enter short tasks count (uint, max 255, note: settings this value to more than the number of total short tasks on the map will result in completing the same task for several times) or exit to return: {Fore.YELLOW}")
            if short_tasks == "exit":
                return None
            try:
                short_tasks = uint(short_tasks)
            except:
                print(f"{Fore.RED}ERROR - Invalid short tasks count! Must be a positive non-floating number (uint).{Fore.WHITE}")
                continue
            hex_data[31] = short_tasks
            success_flag = True
        except Exception as e:
            print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
            continue
    success_flag = False

    return hex_data.hex()



def modify_hide_n_seek_among_us_hex(reference_hex):
    hex_data = bytearray.fromhex(reference_hex)
    success_flag = False

    # Map
    while not success_flag:
        try:
            map = input(f"{Fore.WHITE}Enter map name (Skeld, Mira, Polus, ehT dlekS, Airship, Fungle) or exit to return: {Fore.YELLOW}")
            if map.lower() == "exit":
                return None
            if map.lower() == "eht dleks":
                print(f"{Fore.YELLOW}WARN - Skeld backwards (ehT dlekS) may not work in online lobby!{Fore.WHITE}")
            if map.lower() not in maps.keys():
                print(f"{Fore.RED}ERROR - Invalid map name!{Fore.WHITE}")
                continue
            hex_data[12] = maps[map.lower()]["id"]
            success_flag = True
        except Exception as e:
            print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
            continue
    success_flag = False

    # Player Speed
    while not success_flag:
        try:
            player_speed = input(f"{Fore.WHITE}Enter player speed (float, note: setting this value to more than 3 or less than 0 will only work in local lobbies, public lobby will most likely kick you from the room) or exit to return: {Fore.YELLOW}")
            if player_speed == "exit":
                return None
            try:
                player_speed = float(player_speed)
            except:
                print(f"{Fore.RED}ERROR - Invalid player speed! Must be a floating number (float).{Fore.WHITE}")
                continue
            hex_data[13:17] = struct.pack('<f', player_speed)
            success_flag = True
        except Exception as e:
            print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
            continue
    success_flag = False

    # Hiding Time
    while not success_flag:
        try:
            hiding_time = input(f"{Fore.WHITE}Enter hiding time (float, note: may be incorrect due to among us rounding) or exit to return: {Fore.YELLOW}")
            if hiding_time == "exit":
                return None
            try:
                hiding_time = float(hiding_time)
            except:
                print(f"{Fore.RED}ERROR - Invalid hiding time! Must be a floating number (float).{Fore.WHITE}")
                continue
            hex_data[35:39] = struct.pack('>f', hiding_time)[1::-1] + struct.pack('>f', hiding_time)[3:1:-1] # Mid-Big Endian float for some reason?
            success_flag = True
        except Exception as e:
            print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
            continue
    success_flag = False

    # Crewmate Vision
    while not success_flag:
        try:
            crewmate_vision = input(f"{Fore.WHITE}Enter crewmate vision (float) or exit to return: {Fore.YELLOW}")
            if crewmate_vision == "exit":
                return None
            try:
                crewmate_vision = float(crewmate_vision)
            except:
                print(f"{Fore.RED}ERROR - Invalid crewmate vision! Must be a floating number (float).{Fore.WHITE}")
                continue
            hex_data[17:21] = struct.pack('<f', crewmate_vision)
            success_flag = True
        except Exception as e:
            print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
            continue
    success_flag = False

    # Max Vent Uses
    while not success_flag:
        try:
            vent_uses = input(f"{Fore.WHITE}Enter vent uses count (uint, max 255) or exit to return: {Fore.YELLOW}")
            if vent_uses == "exit":
                return None
            try:
                vent_uses = uint(vent_uses)
            except:
                print(f"{Fore.RED}ERROR - Invalid vent uses count! Must be a positive non-floating number (uint).{Fore.WHITE}")
                continue
            hex_data[29] = vent_uses
            success_flag = True
        except Exception as e:
            print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
            continue
    success_flag = False

    # Max time in vent
    while not success_flag:
        try:
            max_vent_time = input(f"{Fore.WHITE}Enter max time in vent (float, note: may be incorrect due to among us rounding) or exit to return: {Fore.YELLOW}")
            if max_vent_time == "exit":
                return None
            try:
                max_vent_time = float(max_vent_time)
            except:
                print(f"{Fore.RED}ERROR - Invalid max time in vent! Must be a floating number (float).{Fore.WHITE}")
                continue
            hex_data[67:71] = struct.pack('>f', max_vent_time)[1::-1] + struct.pack('>f', max_vent_time)[3:1:-1] # Mid-Big Endian float for some reason again
            success_flag = True
        except Exception as e:
            print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
            continue
    success_flag = False

    # Crewmate Flashlight Size
    while not success_flag:
        try:
            crewmate_flashlight_size = input(f"{Fore.WHITE}Enter crewmate flashlight size (float) or exit to return: {Fore.YELLOW}")
            if crewmate_flashlight_size == "exit":
                return None
            try:
                crewmate_flashlight_size = float(crewmate_flashlight_size)
            except:
                print(f"{Fore.RED}ERROR - Invalid crewmate flashlight size! Must be a floating number (float).{Fore.WHITE}")
                continue
            hex_data[37:41] = struct.pack('<f', crewmate_flashlight_size)
            success_flag = True
        except Exception as e:
            print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
            continue
    success_flag = False

    # Impostor Flashlight Size
    while not success_flag:
        try:
            impostor_flashlight_size = input(f"{Fore.WHITE}Enter impostor flashlight size (float) or exit to return: {Fore.YELLOW}")
            if impostor_flashlight_size == "exit":
                return None
            try:
                impostor_flashlight_size = float(impostor_flashlight_size)
            except:
                print(f"{Fore.RED}ERROR - Invalid impostor flashlight size! Must be a floating number (float).{Fore.WHITE}")
                continue
            hex_data[41:45] = struct.pack('<f', impostor_flashlight_size)
            success_flag = True
        except Exception as e:
            print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
            continue
    success_flag = False

    # Impostor Vision
    while not success_flag:
        try:
            impostor_vision = input(f"{Fore.WHITE}Enter impostor vision (float) or exit to return: {Fore.YELLOW}")
            if impostor_vision == "exit":
                return None
            try:
                impostor_vision = float(impostor_vision)
            except:
                print(f"{Fore.RED}ERROR - Invalid impostor vision! Must be a floating number (float).{Fore.WHITE}")
                continue
            hex_data[21:25] = struct.pack('<f', impostor_vision)
            success_flag = True
        except Exception as e:
            print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
            continue
    success_flag = False

    # Final Hide Time
    while not success_flag:
        try:
            final_time = input(f"{Fore.WHITE}Enter final hide time (float, note: may be incorrect due to among us rounding) or exit to return: {Fore.YELLOW}")
            if final_time == "exit":
                return None
            try:
                final_time = float(final_time)
            except:
                print(f"{Fore.RED}ERROR - Invalid final hide time! Must be a floating number (float).{Fore.WHITE}")
                continue
            hex_data[47:51] = struct.pack('<f', final_time)
            success_flag = True
        except Exception as e:
            print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
            continue
    success_flag = False

    # Final Hide Impostor Speed
    while not success_flag:
        try:
            impostor_speed = input(f"{Fore.WHITE}Enter final hide impostor speed (float) or exit to return: {Fore.YELLOW}")
            if impostor_speed == "exit":
                return None
            try:
                impostor_speed = float(impostor_speed)
            except:
                print(f"{Fore.RED}ERROR - Invalid final hide impostor speed! Must be a floating number (float).{Fore.WHITE}")
                continue
            hex_data[51:55] = struct.pack('<f', impostor_speed)
            success_flag = True
        except Exception as e:
            print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
            continue
    success_flag = False

    # Ping Interval
    while not success_flag:
        try:
            ping_interval = input(f"{Fore.WHITE}Enter ping interval (float) or exit to return: {Fore.YELLOW}")
            if ping_interval == "exit":
                return None
            try:
                ping_interval = float(ping_interval)
            except:
                print(f"{Fore.RED}ERROR - Invalid ping interval! Must be a floating number (float).{Fore.WHITE}")
                continue
            hex_data[63:67] = struct.pack('>f', ping_interval)[1::-1] + struct.pack('>f', ping_interval)[3:1:-1] # I guess almost every seconds setting in hide n seek is Mid-Big Endian float
            success_flag = True
        except Exception as e:
            print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
            continue
    success_flag = False

    # Common Tasks
    while not success_flag:
        try:
            common_tasks = input(f"{Fore.WHITE}Enter common tasks count (uint, max 255, note: settings this value to more than the number of total common tasks on the map will result in completing the same task for several times) or exit to return: {Fore.YELLOW}")
            if common_tasks == "exit":
                return None
            try:
                common_tasks = uint(common_tasks)
            except:
                print(f"{Fore.RED}ERROR - Invalid common tasks count! Must be a positive non-floating number (uint).{Fore.WHITE}")
                continue
            hex_data[25] = common_tasks
            success_flag = True
        except Exception as e:
            print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
            continue
    success_flag = False

    # Long Tasks
    while not success_flag:
        try:
            long_tasks = input(f"{Fore.WHITE}Enter long tasks count (uint, max 255, note: settings this value to more than the number of total long tasks on the map will result in completing the same task for several times) or exit to return: {Fore.YELLOW}")
            if long_tasks == "exit":
                return None
            try:
                long_tasks = uint(long_tasks)
            except:
                print(f"{Fore.RED}ERROR - Invalid long tasks count! Must be a positive non-floating number (uint).{Fore.WHITE}")
                continue
            hex_data[26] = long_tasks
            success_flag = True
        except Exception as e:
            print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
            continue
    success_flag = False

    # Short Tasks
    while not success_flag:
        try:
            short_tasks = input(f"{Fore.WHITE}Enter short tasks count (uint, max 255, note: settings this value to more than the number of total short tasks on the map will result in completing the same task for several times) or exit to return: {Fore.YELLOW}")
            if short_tasks == "exit":
                return None
            try:
                short_tasks = uint(short_tasks)
            except:
                print(f"{Fore.RED}ERROR - Invalid short tasks count! Must be a positive non-floating number (uint).{Fore.WHITE}")
                continue
            hex_data[27] = short_tasks
            success_flag = True
        except Exception as e:
            print(f"{Fore.RED}ERROR - Unexpected error occurred: {e}{Fore.WHITE}")
            continue
    success_flag = False

    return hex_data.hex()

def main():
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
        if hex_output is None: main()
        print(f"Base64 output: {encode_base64(hex_output)} \nHex output (advanced): {hex_output}")
        main()
    elif choice.lower() == "2":
        hex_output = modify_hide_n_seek_among_us_hex(hide_n_seek_ref_hex)
        if hex_output is None: main()
        print(f"Base64 output: {encode_base64(hex_output)} \nHex output (advanced): {hex_output}")
        main()
    elif choice.lower() == "3":
        encode_base64(None)
        main()
    elif choice.lower() == "4":
        decode_base64(None)
        main()
    elif choice.lower() == "5":
        quit()
    else:
        print(f"{Fore.RED}Invalid option!{Fore.WHITE}")
        main()

if __name__ == "__main__":
    print(pyfiglet.figlet_format("Among Us Limit Bypasser", font="modular"))
    print("Copyright (C) 2025 Zaxerf1234")
    print("Full license: https://github.com/Zaxerf1234/AmongUsLimitBypasser/blob/main/LICENSE")
    print(f"Made with love by Zaxerf1234. Version {VERSION} (source code: https://github.com/Zaxerf1234/AmongUsLimitBypasser)")
    main()
