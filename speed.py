import sqlite3

class Speed:
    def __init__(self, db_file='obd_data.db'):
        self.db_file = db_file

    def get_connection(self):
        return sqlite3.connect(self.db_file)

    def get_last_speed_entries(self, limit=10):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT value FROM car_data
            WHERE command = 'SPEED'
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        speed_entries = cursor.fetchall()
        conn.close()
        return speed_entries

    def calculate_average_speed(self, speed_entries):
        total_speed = sum(float(entry[0]) for entry in speed_entries)
        average_speed = total_speed / len(speed_entries)
        return average_speed

    def Avspeed(self):
        speed_entries = self.get_last_speed_entries()
        if speed_entries:
            return self.calculate_average_speed(speed_entries)
        else:
            return None