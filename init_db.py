import sqlite3

with open('schema.ddl') as f:
    schema = f.read()

conn = sqlite3.connect('forum.db')
conn.executescript(schema)
conn.commit()
conn.close()

print("Базу даних створено.")
