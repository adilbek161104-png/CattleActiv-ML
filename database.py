import sqlite3
import os
import sys

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

DB_NAME = os.path.join(application_path, 'cattle_monitoring_v4.db')

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cattle_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cow_id INTEGER NOT NULL,
            steps INTEGER NOT NULL,
            movement_time REAL NOT NULL,
            rumination_minutes INTEGER NOT NULL,
            temperature REAL NOT NULL,
            distance_from_herd REAL NOT NULL,
            lat REAL,
            lng REAL,
            rule_based_result TEXT,
            ml_prediction TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cows_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cow_id INTEGER UNIQUE NOT NULL,
            breed TEXT,
            age INTEGER,
            weight REAL,
            milk_yield REAL,
            image_filename TEXT DEFAULT 'cow1.png',
            registered_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Run migration to add column if it doesn't exist
    try:
        cursor.execute('ALTER TABLE cows_profile ADD COLUMN image_filename TEXT DEFAULT "cow1.png"')
    except sqlite3.OperationalError:
        pass # Column already exists
    
    # Check if empty, seed initial 10 cows
    cursor.execute('SELECT COUNT(*) FROM cows_profile')
    if cursor.fetchone()[0] == 0:
        breeds = ["Golshteyn", "Angus", "Simmental", "Qizil cho'l", "Golshteyn", "Angus", "Simmental", "Golshteyn", "Qizil cho'l", "Angus"]
        for i in range(1, 11):
            breed = breeds[i - 1]
            age = 2 + (i % 4)
            weight = 450 + (i * 15)
            milk = 15 + (i % 5) * 2
            img_name = f"cow{(i % 3) + 1}.png"
            cursor.execute('INSERT INTO cows_profile (cow_id, breed, age, weight, milk_yield, image_filename) VALUES (?, ?, ?, ?, ?, ?)', 
                           (i, breed, age, weight, milk, img_name))

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_settings (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL DEFAULT 'admin',
            password TEXT NOT NULL
        )
    ''')
    
    try:
        cursor.execute('ALTER TABLE admin_settings ADD COLUMN username TEXT NOT NULL DEFAULT "admin"')
    except sqlite3.OperationalError:
        pass # Column already exists
    
    # Check if empty, set default password
    cursor.execute('SELECT COUNT(*) FROM admin_settings')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO admin_settings (id, username, password) VALUES (1, "admin", "admin123")')

    conn.commit()
    conn.close()

def save_prediction(cow_id, steps, movement_time, rumination_minutes, temperature, distance_from_herd, lat, lng, rule_result, ml_pred):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cattle_activity 
        (cow_id, steps, movement_time, rumination_minutes, temperature, distance_from_herd, lat, lng, rule_based_result, ml_prediction)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (cow_id, steps, movement_time, rumination_minutes, temperature, distance_from_herd, lat, lng, rule_result, ml_pred))
    conn.commit()
    conn.close()

def get_all_records():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cattle_activity ORDER BY timestamp DESC LIMIT 100')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_latest_status_by_cow():
    """Har bir qoramol uchun oxirgi statusni qaytaradi"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM cattle_activity 
        WHERE id IN (
            SELECT MAX(id) FROM cattle_activity GROUP BY cow_id
        )
    ''')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
    return [dict(row) for row in rows]

def get_all_cows():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cows_profile ORDER BY cow_id ASC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_cow_profile(cow_id, breed, age, weight, milk_yield, image_filename='cow1.png'):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO cows_profile (cow_id, breed, age, weight, milk_yield, image_filename) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (cow_id, breed, age, weight, milk_yield, image_filename))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False # cow_id already exists
    conn.close()
    return success

def update_cow_profile(cow_id, breed, age, weight, milk_yield, image_filename=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if image_filename:
        cursor.execute('''
            UPDATE cows_profile 
            SET breed=?, age=?, weight=?, milk_yield=?, image_filename=?
            WHERE cow_id=?
        ''', (breed, age, weight, milk_yield, image_filename, cow_id))
    else:
        cursor.execute('''
            UPDATE cows_profile 
            SET breed=?, age=?, weight=?, milk_yield=?
            WHERE cow_id=?
        ''', (breed, age, weight, milk_yield, cow_id))
    
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return success

def delete_cow_profile(cow_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Delete profile
    cursor.execute('DELETE FROM cows_profile WHERE cow_id=?', (cow_id,))
    # Delete history
    cursor.execute('DELETE FROM cattle_activity WHERE cow_id=?', (cow_id,))
    
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return success

if __name__ == '__main__':
    init_db()
    print("Yangi ma'lumotlar bazasi va jadvallar muvaffaqiyatli yaratildi/yangilandi.")

def check_credentials(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT username, password FROM admin_settings WHERE id = 1')
    row = cursor.fetchone()
    conn.close()
    if row and row['username'] == username and row['password'] == password:
        return True
    return False

def check_password(password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM admin_settings WHERE id = 1')
    row = cursor.fetchone()
    conn.close()
    if row and row['password'] == password:
        return True
    return False

def update_password(new_password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE admin_settings SET password = ? WHERE id = 1', (new_password,))
    conn.commit()
    conn.close()
    return True
