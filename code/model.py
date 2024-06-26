import sqlite3
import uuid
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
class Model:
    def __init__(self):
        self.conn = sqlite3.connect(resource_path("components.db"))
        self.c = self.conn.cursor()
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS Component
                          (id text PRIMARY KEY, tag text, description text)"""
        )
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS Repair
                          (repair_id text PRIMARY KEY, time_between_fails text, repair_time text, component_id text, tbf_unit text, rt_unit text,
                          FOREIGN KEY(component_id) REFERENCES Component(id))"""
        )

    def register_component(self, tag, description):
        id = str(uuid.uuid4())
        self.c.execute("INSERT INTO Component VALUES (?, ?, ?)", (id, tag, description))
        self.conn.commit()
        return id, tag, description

    def register_repairs(self, repairs):
        for repair in repairs:
            repair_id = repair["repair_id"]
            time_between_fails = repair["time_between_fails"]
            repair_time = repair["repair_time"]
            component_id = repair["component_id"]
            tbf_unit = repair["tbf_unit"]
            rt_unit = repair["rt_unit"]
            self.c.execute(
                "INSERT INTO Repair VALUES (?, ?, ?, ?, ?, ?)",
                (
                    repair_id,
                    time_between_fails,
                    repair_time,
                    component_id,
                    tbf_unit,
                    rt_unit,
                ),
            )
        self.conn.commit()

    def select_tbf_data(self, component_id):
        data = []
        tbf_unit = None
        try:
            self.c.execute(
                "SELECT time_between_fails, tbf_unit FROM Repair WHERE component_id = ?",
                (component_id,),
            )
            rows = self.c.fetchall()
            if rows:
                data = [row[0] for row in rows]
                tbf_unit = rows[0][1]
        except sqlite3.Error as e:
            print("Error while fetching TBF data:", e)
        finally:
            return data, tbf_unit
