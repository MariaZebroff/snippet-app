from PyQt6.QtWidgets import *
from PyQt6 import uic
import sys
from snippet_manager import SnippetManager

class AddSnippetDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("addsnippetdialog.ui", self)
        self.load_categories()
        self.checkBox.stateChanged.connect(self.on_checkbox_changed)
        self.CloseSnipButton.clicked.connect(self.close)
        self.saveSnipButton.clicked.connect(self.save_snippet)
        
    def load_categories(self):
        """Fetch categories from the database and populate the ComboBox."""
        # Assuming SnippetManager has a method to fetch categories
        categories = SnippetManager.get_categories()  # This should return a list of category names
        
        # Add categories to ComboBox
        self.categoryComboBox.clear()
        for category in categories:
            self.categoryComboBox.addItem(category.title())
            
    def on_checkbox_changed(self, state):
        if self.checkBox.isChecked():
            self.newCatLineEdit.setEnabled(True)
            self.categoryComboBox.setEnabled(False)
        else:
            self.newCatLineEdit.setEnabled(False)
            self.categoryComboBox.setEnabled(True)
            
    def save_snippet(self):
        category = ''
        title = ''
        content = ''
        if self.checkBox.isChecked():
            category = self.newCatLineEdit.text()
        else:
           index = self.categoryComboBox.currentIndex()
           category =self.categoryComboBox.itemText(index) 
        print('Cat', category)
        snippet_title=self.titleLineEdit.text()
        print('Title', snippet_title)
        snippet_body=self.textEdit.toPlainText()
        print('Body', snippet_body)
        if snippet_title == '' or snippet_body == '' or category == '':
            print('Pop up filds are empty')
        else:
            SnippetManager.create(title=snippet_title, content=snippet_body, category=category)
            self.close()
        
if __name__ == "__main__":
    app = QApplication([])
    window = AddSnippetDialog()
    window.show()
    sys.exit(app.exec())
