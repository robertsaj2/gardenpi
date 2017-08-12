import sqlite3

if __name__ == '__main__':
    connection = sqlite3.connect('temperature.db')
    cursor = connection.cursor()
    cursor.execute("create table temperature_humidity (temperature real, humidity real, created_at timestamp);")
    connection.commit()
    connection.close()
