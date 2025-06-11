import subprocess
import re

def get_keyboard_layout() -> str:
    """Detects the current keyboard layout ('en' or 'ru') on X11."""
    try:
        result = subprocess.check_output(
            ["xset", "-q"],
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Primary Method: Check for "Group 2: on/off"
        indicator_match = re.search(r"Group 2:\s+(on|off)", result)
        if indicator_match:
            return "ru" if indicator_match.group(1) == "on" else "en"

        # Fallback Method: Check for "effective" group index
        group_match = re.search(r"group\s(\d+):\s+.*\(effective\)", result)
        if group_match:
            return "ru" if int(group_match.group(1)) > 0 else "en"

    except FileNotFoundError:
        print("Error: 'xset' command not found. Cannot detect keyboard layout.")
    except Exception as e:
        print(f"An error occurred while detecting keyboard layout: {e}")
    
    print("Warning: Keyboard layout detection failed. Defaulting to 'ru'.")
    return "ru" 