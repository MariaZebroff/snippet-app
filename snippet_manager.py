"""Snippet class for creating and updating new information"""
from snippet_db_connection import con,cur
import datetime


class SnippetManager:

    @staticmethod  
    def create(title, content, category, is_encrypted=False):
        now = datetime.datetime.now()
        cur.execute("INSERT INTO snippets (title, content, category, is_encrypted, created_at) VALUES (?, ?, ?, ?, ?)", 
                    (title, content, category, is_encrypted, now))
        con.commit()
        return cur.lastrowid

    @staticmethod
    def find_by_id(id):
        cur.execute("SELECT * FROM snippets WHERE id == ?", (id,))
        return cur.fetchone()
        
    @staticmethod
    def find_by_category(category):
        cur.execute("SELECT * FROM snippets WHERE category == ?", (category,))
        return cur.fetchall()
    
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
        cur.execute("DELETE FROM snippets WHERE id == ?", (id,))
        con.commit()
    
        if cur.rowcount > 0:
            print(f"Snippet {id} deleted.")
        else:
            print(f"Snippet {id} not found.")
    

snippets = SnippetManager.search_by_content("My")
print("Snippets in Updated Category:", snippets)