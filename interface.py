
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShortcut, QKeySequence, QPainter, QColor, QPixmap, QIcon
from PyQt6 import uic
import pandas as pd

from utils import *
from snippet_manager import SnippetManager
from add_snippet_dialog import AddSnippetDialog


def create_color_icon(color: QColor, size=10):
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    painter.setBrush(color)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRect(0, 0, size, size)
    painter.end()
    
    return QIcon(pixmap)




class SMGUI(QMainWindow):
    def __init__(self):
        super(SMGUI, self).__init__()
        uic.loadUi(resource_path("mainwindow.ui"), self)
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
        
        shortcut = QShortcut(QKeySequence("Meta+C"), self)
        shortcut.setContext(Qt.ShortcutContext.ApplicationShortcut)
        shortcut.activated.connect(lambda: self.copy_snippet())
        #Manu Export
        self.actionExport.triggered.connect(self.export_data)
        self.actionImport.triggered.connect(self.import_data)
        self.actionClose.triggered.connect(self.close)
        self.show()
        
    def load_snippets(self,snip, row=0):
        """Load snippet titles from the database into the QListWidget."""
        snippets = snip
        self.listWidget.clear()
        
        for snippet in snippets:
            item = QListWidgetItem(snippet[1])  # snippet[1] = title
            item.setData(256, snippet)  # Store full snippet data in the item
            category = snippet[3]
            print('category', category)
            color_str = SnippetManager.find_color(category)
            print('color_str', color_str)
            if color_str:
                color = QColor(color_str)
                color_str = color.name()
                item.setIcon(create_color_icon(color))
            self.listWidget.addItem(item)
        
        if snippets:
         currentRow = self.listWidget.setCurrentRow(row)
         print('currentRow from load snip', currentRow)
         corresponding_snippet = self.listWidget.item(row)
         print('corresponding_snippet from load snip', corresponding_snippet)
         self.display_snippet_content(corresponding_snippet)

    def display_snippet_content(self, item):
        """Display snippet content when a title is clicked."""
        if item != None:
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
            
    def display_by_category(self, index, snip_index=0):
        self.snippetTextEdit.clear()
        self.listWidget.clear()
        category = self.category.itemText(index)
        snip_by_cat= SnippetManager.find_by_category(category)
        self.load_snippets(snip_by_cat, snip_index)
        print(f"Category clicked: {category}")
        
    
    # Buttons 
    def add_snippet(self):
         dialog = AddSnippetDialog(self)
         res=dialog.exec()
         
         if res == QDialog.DialogCode.Accepted:
            row = self.listWidget.count()
            self.load_snippets(SnippetManager.find_all())
            self.load_categories()
            self.display_by_category(0, row)
            print('Accepted')
         
         
    def save_edits(self,item):
        current_item = self.listWidget.currentItem()
        current_item_index = self.listWidget.currentRow()

        if current_item:
            # Get the text of the item
            print(f"Item Text: {current_item.text()}")
            
            # Get the custom data you've set (e.g., full snippet data) stored in the item
            snippet_data = current_item.data(256)  # The 256 is the role that you set for storing custom data
            if snippet_data:
                new_content=self.snippetTextEdit.toPlainText()
                if new_content != '':
                    SnippetManager.update(snippet_data[0], content=new_content)
                    show_action_text(self.editButton, "Saved!")
                    cur_cat_index = self.category.currentIndex()
                    self.display_by_category(cur_cat_index, current_item_index)
                else:
                   show_popup_message("Snippet cannot be empty!")
                                        
    def delete_snippet(self,item):
        current_item = self.listWidget.currentItem()
        current_item_index = self.listWidget.currentRow()
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
            prev_item = current_item_index - 1
            print('prev_item', prev_item)
            if index != -1 and current_index_of_category_drop_down != 0:
                self.category.setCurrentIndex(index)
                self.display_by_category(index, prev_item)
            else: 
                self.display_by_category(0, prev_item)
                
    def copy_snippet(self):
        snippet_body_text = self.snippetTextEdit.toPlainText()
        copy_to_clipboard(snippet_body_text)
        show_action_text(self.copyButton, "Copied to clipboard!")
        
    def export_data(self):
        all_snippets = SnippetManager.find_all()
        data = []
        for snippet in all_snippets:
            clean_obj = {'id': snippet[0], 'title': snippet[1], 'snippet': snippet[2], 'category': snippet[3], 'date': snippet[5]}
            data.append(clean_obj)
        self.save_csv_dialog(data) 
        
    def import_data(self):
        try:
            # Open file dialog to select CSV
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Open CSV File",
                "",
                "CSV Files (*.csv);;All Files (*)"
            )
            
            if file_path:
                
                df = pd.read_csv(file_path)
                
                # Convert ENTIRE DataFrame to list of dictionaries
                all_data = df.to_dict('records') 
                try:
                    SnippetManager.bulk_load(all_data)
                    snips = SnippetManager.find_all()
                    self.load_snippets(snips)
                    print(f"Success! Loaded {len(all_data)} rows.")
                    self.statusBar().showMessage(f"Success! Loaded {len(all_data)} rows.", 5000)
                except Exception as e:
                    print(f"Error: {e}")
                    self.statusBar().showMessage("Something went wrong! Check your file.", 5000)       
                
                # print(all_data)  # Full data as dictionaries
                
                # return all_data  # Return all rows as dictionaries
                
        except Exception as e:
            print(f"Error: {e}")
            return None
        
    def save_csv_dialog(self,data):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save CSV",
            "",  # Default directory or filename
            "CSV Files (*.csv);;All Files (*)"
        )

        if filename:
            export_to_csv(data, filename)
        
                

def main():
    app=QApplication([])
    window=SMGUI()
    app.exec()

if __name__ == '__main__':
    main()