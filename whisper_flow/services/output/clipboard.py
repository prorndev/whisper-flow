import pyperclip

def copy_to_clipboard(text: str):
    """Copies text to the system clipboard."""
    try:
        pyperclip.copy(text)
        print("Text copied to clipboard.")
    except pyperclip.PyperclipException as e:
        print(f"Error copying to clipboard: {e}") 