import sqlite3

con=sqlite3.connect(f'./snippet_db.db')
cur = con.cursor()

#Table created 

# cur.execute("""
#     CREATE TABLE snippets (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         title TEXT,
#         content TEXT,
#         category TEXT,
#         is_encrypted BOOLEAN,
#         created_at DATETIME DEFAULT CURRENT_TIMESTAMP
#     )
# """)

# Export `cur` and `con`
__all__ = ['con', 'cur']