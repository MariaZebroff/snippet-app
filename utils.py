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
    """Get the correct path to the database file, ensuring it's in a writable location"""
    if getattr(sys, 'frozen', False):
        # Running in PyInstaller bundle
        base_path = Path(sys._MEIPASS)
        
        # Get user's application data directory
        if sys.platform == 'win32':
            import appdirs
            app_data_dir = Path(appdirs.user_data_dir(appauthor="YourCompany", appname="YourApp"))
        else:
            app_data_dir = Path.home() / ".your_app_name"
            
        app_data_dir.mkdir(parents=True, exist_ok=True)
        db_destination = app_data_dir / "snippet_db.db"
        
        # Copy initial database if it doesn't exist
        if not db_destination.exists():
            bundled_db = base_path / "snippet_db.db"
            if bundled_db.exists():
                import shutil
                shutil.copyfile(bundled_db, db_destination)
        
        return db_destination
    else:
        # Running in development
        return Path(__file__).parent / "snippet_db.db"