"""Snippet class for creating and updating new information"""
from snippet_db_connection import con,cur
import datetime


class SnippetManager:

    @staticmethod  
    def create(title, content, category, color='cccccc', is_encrypted=False):
        now = datetime.datetime.now()
        formated_category = category.lower().title()
        cur.execute("INSERT INTO snippets (title, content, category, is_encrypted, created_at) VALUES (?, ?, ?, ?, ?)", 
                    (title, content, formated_category, is_encrypted, now))
        con.commit()
        cur.execute("SELECT * FROM colors WHERE category = ?", (formated_category,))
        row_existing = cur.fetchone()
        if not row_existing:
            cur.execute("INSERT INTO colors (category, color) VALUES (?, ?)", 
                    (formated_category, color))
            con.commit()
        
        return cur.lastrowid

    @staticmethod
    def find_by_id(id):
        cur.execute("SELECT * FROM snippets WHERE id == ?", (id,))
        return cur.fetchone()
        
    @classmethod
    def find_by_category(cl,category):
        if category == "All":
            res = cl.find_all()
            return res
        else:
            formated_category = category.lower().title()
            cur.execute("SELECT * FROM snippets WHERE category == ?", (formated_category,))
            res_cat = cur.fetchall()
            return res_cat
    
    @staticmethod
    def search_by_content(str):
        cur.execute("SELECT * FROM snippets WHERE (content LIKE ? OR title LIKE ?)", (f'%{str}%',f'%{str}%'))
        data = cur.fetchall()
        if len(data) != 0:
            return data
        else:
            return "Not found"
    
    @staticmethod
    def find_all():
        cur.execute("SELECT * FROM snippets")
        return cur.fetchall()
    
    @staticmethod
    def get_categories():
        cur.execute("SELECT category FROM snippets")
        raw_cat = cur.fetchall()
        unique_categories = set(category[0] for category in raw_cat)
        return unique_categories
    
    @staticmethod
    def update(id, title=None, content=None, category=None, is_encrypted=None):
        """Update snippet by ID, only updating provided fields."""
        now = datetime.datetime.now()
        
    
        cur.execute("""
            UPDATE snippets 
            SET 
                title = COALESCE(?, title), 
                content = COALESCE(?, content), 
                category = COALESCE(?, category), 
                is_encrypted = COALESCE(?, is_encrypted),
                created_at = ?
            WHERE id == ?
        """, (title, content, category, is_encrypted, now, id))
        
        con.commit()
        
        print(f"Snippet {id} updated.")

    @staticmethod
    def delete(id):
        """Delete snippet by ID."""
        cur.execute("SELECT category FROM snippets WHERE id = ?", (id,))
        deleted_snip_cat_row = cur.fetchone()

        if not deleted_snip_cat_row:
            print(f"Snippet {id} not found.")
            return

        deleted_snip_cat = deleted_snip_cat_row[0]

        cur.execute("DELETE FROM snippets WHERE id = ?", (id,))
        con.commit()

        cur.execute("SELECT * FROM snippets WHERE category = ?", (deleted_snip_cat,))
        row_existing = cur.fetchone()

        if not row_existing:
            cur.execute("DELETE FROM colors WHERE category = ?", (deleted_snip_cat,))
            con.commit()

        print(f"Snippet {id} deleted.")

    
    @staticmethod        
    def find_color(category):
        formated_category = category.lower().title()
        cur.execute("SELECT color FROM colors WHERE category = ?", (formated_category,))
        row = cur.fetchone()
        if row:
            return row[0]  # return only the color string
        return None
        
# color = SnippetManager.find_color('3')  
# print(color)

# SnippetManager.create("title", "content1", "2", '#cccccc')
# SnippetManager.delete(434)
# SnippetManager.delete(435)
# snippets = SnippetManager.search_by_content("My")
# print("Snippets in Updated Category:", snippets)
# SnippetManager.create("title", "content1", "Testcategory1")
# SnippetManager.create("title", "content1", "Testcategory1")
# SnippetManager.create("title", "content1", "Test3category1")
# SnippetManager.create("title", "content1", "category1")
# SnippetManager.create("title", "content1", "cCategory1")


# cat = SnippetManager.get_categories()
# print("Snippets in Updated Category:", cat)