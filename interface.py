from PyQt6.QtWidgets import *
from PyQt6 import uic
from snippet_manager import SnippetManager

class SMGUI(QMainWindow):
    def __init__(self):
        super(SMGUI, self).__init__()
        uic.loadUi("mainwindow.ui", self)
        self.load_snippets(SnippetManager.find_all())
        self.load_categories()
        # Connect the item click event
        self.listWidget.itemClicked.connect(self.display_snippet_content)
        self.category.currentIndexChanged.connect(self.display_by_category)
        # self.snippetTextEdit.textChanged.connect(self.on_snippet_text_changed)
        
        self.editButton.clicked.connect(self.save_edits)
        self.deleteButton.clicked.connect(self.delete_snippet)
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
                    SnippetManager.update(snippet_data[0], title=None, content=new_content, category=None, is_encrypted=None)
                    cur_cat_index = self.category.currentIndex()
                    self.display_by_category(cur_cat_index)
                else:
                    print('Pop up window')
                    
    def delete_snippet(self,item):
        current_item = self.listWidget.currentItem()
        id = current_item.data(256)[0]
        if current_item:
            former_cat=SnippetManager.find_by_id(id)[3]
            SnippetManager.delete(id)
            print('former_cat',former_cat)
            self.load_snippets(SnippetManager.find_all())
            self.load_categories()
            index = self.category.findText(former_cat)
            if index != -1:
                self.display_by_category(index)
                self.category.setCurrentIndex(index)
            else: 
                self.display_by_category(0)

def main():
    app=QApplication([])
    window=SMGUI()
    app.exec()

if __name__ == '__main__':
    main()