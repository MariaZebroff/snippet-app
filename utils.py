from PyQt6.QtWidgets import QToolTip, QMessageBox
import pyperclip

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