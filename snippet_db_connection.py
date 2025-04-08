import sqlite3
from pathlib import Path
from utils import *


db_path = get_db_path()
con=sqlite3.connect(str(db_path))
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