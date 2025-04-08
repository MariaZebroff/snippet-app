import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QToolTip, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import pyperclip
import csv

def show_action_text(elem, message):
    pos = elem.mapToGlobal(elem.rect().topRight())
    pos.setY(pos.y() - 50)
    QToolTip.showText(pos, message)
    
def show_popup_message(user_message):
    message = QMessageBox()
    message.setText(user_message)
    message.exec()

       
def copy_to_clipboard(text):
    pyperclip.copy(text)
    
def export_to_csv(data, filename):
    """
    Exports a list of dictionaries to a CSV file.

    :param data: List of dictionaries (e.g., [{'name': 'Alice', 'age': 30}, ...])
    :param filename: Name of the output CSV file
    """
    if not data:
        print("No data to export.")
        return

    fieldnames = data[0].keys()  # Use keys from first item as CSV headers

    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Data exported to {filename}")
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def get_db_path():
    """Get the correct path to the database file in both dev and bundled mode"""
    if getattr(sys, 'frozen', False):
        # Running in PyInstaller bundle
        base_path = Path(sys._MEIPASS)
    else:
        # Running in development
        base_path = Path(__file__).parent
    
    return base_path / "snippet_db.db"