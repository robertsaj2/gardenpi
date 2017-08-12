import RPi.GPIO as GPIO
import dht11
import time
import sqlite3
from datetime import datetime

pin = 7
GPIO.setmode(GPIO.BOARD)

instance = dht11.DHT11(pin=pin)
result = instance.read()
while True:
    if result.is_valid():
        temperature = result.temperature*9.00/5+32
        now = datetime.now()
        connection = sqlite3.connect('temperature.db')
        cursor = connection.cursor()
        cursor.execute("insert into temperature_humidity values (?,?,?)", (temperature,result.humidity,now))

        connection.commit()
        connection.close()
    time.sleep(60)
GPIO.cleanup()
