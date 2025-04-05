from PyQt6.QtWidgets import *
from PyQt6 import uic
import pyperclip
from snippet_manager import SnippetManager
from add_snippet_dialog import AddSnippetDialog

class SMGUI(QMainWindow):
    def __init__(self):
        super(SMGUI, self).__init__()
        uic.loadUi("mainwindow.ui", self)
        self.setWindowTitle("Code Snippet Manager")
        self.load_snippets(SnippetManager.find_all())
        self.load_categories()
        # Connect the item click event
        self.listWidget.itemClicked.connect(self.display_snippet_content)
        self.category.currentIndexChanged.connect(self.display_by_category)
        # self.snippetTextEdit.textChanged.connect(self.on_snippet_text_changed)
        
        self.editButton.clicked.connect(self.save_edits)
        self.deleteButton.clicked.connect(self.delete_snippet)
        self.addButton.clicked.connect(self.add_snippet)
        self.copyButton.clicked.connect(self.copy_snippet)
        self.show()
        
    def load_snippets(self,snip):
        """Load snippet titles from the database into the QListWidget."""
        snippets = snip
        self.listWidget.clear()
        
        for snippet in snippets:
            item = QListWidgetItem(snippet[1])  # snippet[1] = title
            item.setData(256, snippet)  # Store full snippet data in the item
            self.listWidget.addItem(item)
        
        if snippets:
         self.listWidget.setCurrentRow(0)
         first_snip = self.listWidget.item(0)
         self.display_snippet_content(first_snip)

    def display_snippet_content(self, item):
        """Display snippet content when a title is clicked."""
        snippet = item.data(256)  # Retrieve full snippet data
        self.snippetTextEdit.setPlainText(snippet[2])
        
    def load_categories(self):
        """Fetch categories from the database and populate the ComboBox."""
        # Assuming SnippetManager has a method to fetch categories
        categories = SnippetManager.get_categories()  # This should return a list of category names
        
        # Add categories to ComboBox
        self.category.clear()  # Clear any existing items
        self.category.addItem('All')
        for category in categories:
            self.category.addItem(category.title())
            
    def display_by_category(self, index):
        self.snippetTextEdit.clear()
        self.listWidget.clear()
        category = self.category.itemText(index)
        snip_by_cat= SnippetManager.find_by_category(category)
        self.load_snippets(snip_by_cat)
        print(f"Category clicked: {category}")
        
    
    # Buttons 
    def add_snippet(self):
         dialog = AddSnippetDialog(self)
         dialog.exec()
         
         
    def save_edits(self,item):
        print('Save button clicked!')
        print(item)
        current_item = self.listWidget.currentItem()

        if current_item:
            # Get the text of the item
            print(f"Item Text: {current_item.text()}")
            
            # Get the custom data you've set (e.g., full snippet data) stored in the item
            snippet_data = current_item.data(256)  # The 256 is the role that you set for storing custom data
            if snippet_data:
                new_content=self.snippetTextEdit.toPlainText()
                if snippet_data != new_content and new_content != '':
                    SnippetManager.update(snippet_data[0], content=new_content)
                    cur_cat_index = self.category.currentIndex()
                    self.display_by_category(cur_cat_index)
                else:
                    print('Pop up window')
                    
    def delete_snippet(self,item):
        current_item = self.listWidget.currentItem()
        id = current_item.data(256)[0]
        if current_item:
            former_cat=SnippetManager.find_by_id(id)[3]
            current_index_of_category_drop_down =  self.category.currentIndex()
            print('former cat',former_cat)
            print('current_index_of_category_drop_down',current_index_of_category_drop_down)
            SnippetManager.delete(id)
            self.load_snippets(SnippetManager.find_all())
            self.load_categories()
            index = self.category.findText(former_cat)
            if index != -1 and current_index_of_category_drop_down != 0:
                self.display_by_category(index)
                self.category.setCurrentIndex(index)
            else: 
                self.display_by_category(0)
                
    def copy_snippet(self):
        snippet_body_text = self.snippetTextEdit.toPlainText()
        self.copy_to_clipboard(snippet_body_text)
        pos = self.copyButton.mapToGlobal(self.copyButton.rect().topRight())
        pos.setY(pos.y() - 50)
        QToolTip.showText(pos, "Copied to clipboard!")

    @staticmethod          
    def copy_to_clipboard(text):
        pyperclip.copy(text)
                

def main():
    app=QApplication([])
    window=SMGUI()
    app.exec()

if __name__ == '__main__':
    main()