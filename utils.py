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
        
snippets = [
    {"title": "Hello World", "content": "print('Hello, World!')", "category": "Python"},
    {"title": "List Comprehension", "content": "[x*x for x in range(5)]", "category": "Python"},
]

export_to_csv(snippets, "snippets.csv")