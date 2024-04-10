import sqlite3
import uuid

class Model:
    def __init__(self):
        self.conn = sqlite3.connect('components.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS Component
                          (id text PRIMARY KEY, tag text, description text)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS Repair
                          (repair_id text PRIMARY KEY, time_between_fails text, repair_time text, component_id text,
                          FOREIGN KEY(component_id) REFERENCES Component(id))''')

    def register_component(self, tag, description):
        id = str(uuid.uuid4())
        self.c.execute("INSERT INTO Component VALUES (?, ?, ?)", (id, tag, description))
        self.conn.commit()
        return id, tag, description