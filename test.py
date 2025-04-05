import pyperclip

def copy_to_clipboard(text):
    pyperclip.copy(text)
    print("Copied to clipboard!")

# Example usage:
copy_to_clipboard("Hello from Python!")