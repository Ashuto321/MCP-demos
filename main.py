from fastmcp import FastMCP
import os
import sqlite3

#writing the db path for storing the sqlite in out folder
DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")

# creating the instance of the mcp
mcp = FastMCP("Expense Tracker")


# initiatizing the db
def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""
                  
                  CREATE TABLE IF NOT EXISTS expenses(
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      date TEXT NOT NULL,
                      amount REAL NOT NULL,
                      category TEXT NOT NULL,
                      subcategory TEXT DEFAULT '',
                      note TEXT DEFAULT ''
                      )
                """)
#calling the functionn        
init_db()


# now we will create the tools!
@mcp.tool()
def add_expense(date, amount, category, subcategory="", note=""):
    
    ''' Add a new expense entry to the database'''
    
    with sqlite3.connect(DB_PATH) as c:
        curr = c.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES(?,?,?,?,?)", 
            (date, amount, category, subcategory, note)
        )
        return {"status": "ok", "id": curr.lastrowid}
    
@mcp.tool()
def list_expense(START_DATE, END_DATE):
    
    ''' Show all the transaction in the database '''
    
    with sqlite3.connect(DB_PATH) as c:
        curr = c.execute("SELECT id, date, amount, category, subcategory, note FROM expenses WHERE BETWEEN ? AND ? ORDER BY id ASC"), (START_DATE, END_DATE)
        cols =[d[0] for d in curr.description]
        return [dict(zip(cols, r)) for r in curr.fetchall()]
    
if __name__ == "__main__":
    mcp.run()