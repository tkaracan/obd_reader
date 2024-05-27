import sqlite3

class DbReader:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        # Create first data for comparison
        self.first_data = {'av_fuel_level': None, "last_mile": None}
        if self.first_data['av_fuel_level'] is None:
            self.first_data['av_fuel_level'] = self.get_average_of_last_n_entries("FUEL_LEVEL", 10)
        if self.first_data['last_mile'] is None:
            self.first_data['last_mile'] = self.get_latest_entry("DISTANCE_SINCE_DTC_CLEAR")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

    def get_latest_entry(self, command_name):
        query = '''
            SELECT value FROM car_data
            WHERE command = ?
            ORDER BY timestamp DESC
            LIMIT 1
        '''
        self.cursor.execute(query, (command_name,))
        row = self.cursor.fetchone()
        if row:
            try:
                # Convert the value directly to float
                return float(row[0])
            except ValueError:
                print(f"Error converting {row[0]} to float")
                return None
        return None

    def get_av_data(self, command_name, n=10):
        query = f'''
            SELECT value FROM car_data
            WHERE command = ?
            ORDER BY timestamp DESC
            LIMIT ?
        '''
        self.cursor.execute(query, (command_name, n))
        rows = self.cursor.fetchall()
        values = []
        for row in rows:
            try:
                # Attempt to convert the value directly to float
                numeric_value = float(row[0])
                values.append(numeric_value)
            except ValueError:
                # If conversion fails, log or handle the error appropriately
                print(f"Error converting {row[0]} to float")
        if values:
            average = sum(values) / len(values)
            return round(average, 2)  # Round the result to two decimal places
        else:
            return 0

    def get_average_of_last_n_entries(self, command_name, n):
        last_n_entries = self.get_av_data(command_name, n)
        return last_n_entries

if __name__ == "__main__":
    # Example usage
    with DbReader('obd_readings.db') as db_reader:
        avg_fuel_level = db_reader.get_average_of_last_n_entries("FUEL_LEVEL", 10)
        print(f"Average of last 10 FUEL LEVEL entries: {avg_fuel_level}")
        last_mile = db_reader.get_latest_entry("DISTANCE_SINCE_DTC_CLEAR")
        print(f"Latest DISTANCE_SINCE_DTC_CLEAR entry: {last_mile}")
