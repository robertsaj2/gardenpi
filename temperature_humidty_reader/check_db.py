import sqlite3

connection = sqlite3.connect('temperature.db')
cursor = connection.cursor()
cursor.execute('select * from temperature_humidity')
rows = cursor.fetchall()

print(len(rows))