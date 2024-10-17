import sqlite3

# Use the full path to your SQLite database
conn = sqlite3.connect(r'C:\Users\abiji\Desktop\project-root\instance\health.db')  
cursor = conn.cursor()

# Execute a query to retrieve the names of all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Print the names of the tables
print(tables)

# Close the connection
conn.close()
