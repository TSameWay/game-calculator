import sqlite3
import json

DB_FILE = 'game_data.db'

class DataManager:
    def __init__(self):
        self.db_file = DB_FILE
        self.create_tables()
        self.init_default_data()

    def create_tables(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                base_level INTEGER DEFAULT 1
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS saved_characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_id INTEGER NOT NULL,
                character_name TEXT NOT NULL,
                calculation_data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (character_id) REFERENCES characters (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS player_resources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resource_name TEXT UNIQUE NOT NULL,
                amount INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS character_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_id INTEGER NOT NULL,
                plan_name TEXT NOT NULL,
                resources_needed TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (character_id) REFERENCES characters (id)
            )
        ''')
        
        conn.commit()
        conn.close()

    def init_default_data(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM characters")
        count = cursor.fetchone()[0]
        
        if count == 0:
            default_characters = [
                (1, 'Anby Demara', 1),
                (2, 'Billy Kid', 1),
                (3, 'Nicole Demara', 1),
                (4, 'Koleda Belobog', 1)
            ]
            
            cursor.executemany(
                "INSERT INTO characters (id, name, base_level) VALUES (?, ?, ?)",
                default_characters
            )

        cursor.execute("SELECT COUNT(*) FROM player_resources")
        resource_count = cursor.fetchone()[0]
        
        if resource_count == 0:
            default_resources = [
                ('Dennies', 0), ('Senior Investigator Log', 0),
                ('Basic Support Certification Seal', 0), ('Advanced Support Certification Seal', 0),
                ('Ruler Certification Seal', 0), ('Purple boss material', 0),
                ('Gold boss material', 0), ('Basic Chip', 0),
                ('Advanced Chip', 0), ('Specialized Chip', 0),
                ('Hamster Cage Pass', 0)
            ]
            
            cursor.executemany(
                "INSERT INTO player_resources (resource_name, amount) VALUES (?, ?)",
                default_resources
            )
        
        conn.commit()
        conn.close()

    def get_characters(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, base_level FROM characters")
        characters = [{'id': row[0], 'name': row[1], 'base_level': row[2]} for row in cursor.fetchall()]
        conn.close()
        return characters

    def get_saved_characters(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT id, character_id, character_name, calculation_data, created_at FROM saved_characters ORDER BY created_at DESC')
        saved_chars = [{'id': row[0], 'character_id': row[1], 'name': row[2], 'data': row[3], 'created_at': row[4]} for row in cursor.fetchall()]
        conn.close()
        return saved_chars

    def save_character(self, character_data):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM saved_characters WHERE character_name = ?', (character_data['name'],))
        count = cursor.fetchone()[0]
        character_name = f"{character_data['name']} #{count + 1}" if count > 0 else character_data['name']
        cursor.execute('INSERT INTO saved_characters (character_id, character_name, calculation_data) VALUES (?, ?, ?)',
                     (character_data['character_id'], character_name, json.dumps(character_data['data'])))
        conn.commit()
        conn.close()

    def delete_character(self, char_id):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM saved_characters WHERE id = ?", (char_id,))
        conn.commit()
        conn.close()

    def get_player_resources(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT resource_name, amount FROM player_resources")
        resources = {row[0]: row[1] for row in cursor.fetchall()}
        conn.close()
        return resources

    def update_resource(self, resource_name, amount):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO player_resources (resource_name, amount, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)',
                     (resource_name, amount))
        conn.commit()
        conn.close()

    def save_character_plan(self, character_id, plan_name, resources_needed):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO character_plans (character_id, plan_name, resources_needed) VALUES (?, ?, ?)',
                     (character_id, plan_name, json.dumps(resources_needed)))
        conn.commit()
        conn.close()

    def get_character_plans(self, character_id=None):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        if character_id:
            cursor.execute('''
                SELECT cp.id, cp.character_id, cp.plan_name, cp.resources_needed, cp.created_at, c.name
                FROM character_plans cp JOIN characters c ON cp.character_id = c.id
                WHERE cp.character_id = ? ORDER BY cp.created_at DESC
            ''', (character_id,))
        else:
            cursor.execute('''
                SELECT cp.id, cp.character_id, cp.plan_name, cp.resources_needed, cp.created_at, c.name
                FROM character_plans cp JOIN characters c ON cp.character_id = c.id
                ORDER BY cp.created_at DESC
            ''')
        plans = [{
            'id': row[0], 'character_id': row[1], 'plan_name': row[2],
            'resources_needed': json.loads(row[3]), 'created_at': row[4], 'character_name': row[5]
        } for row in cursor.fetchall()]
        conn.close()
        return plans

    def delete_plan(self, plan_id):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM character_plans WHERE id = ?", (plan_id,))
        conn.commit()
        conn.close()