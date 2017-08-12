import RPi.GPIO as GPIO
import dht11
import time
import sqlite3

connection = sqlite3.connect('temperature.db')
cursor = connection.cursor()

cursor.execute("create table temperature_humidity (temperature real, humidity real);")

pin = 7
GPIO.setmode(GPIO.BOARD)

for i in range(60):
    instance = dht11.DHT11(pin=pin)
    result = instance.read()

    if result.is_valid():
        temperature = result.temperature*9/5+32
        print("The temperature is: %d" % int(temperature))
        print("The humidity is: %d" % result.humidity)
        print("=================")
        cursor.execute("insert into temperature_humidity (temperature, humidity) values (%d,%d);" % (temperature,result.humidity))
    time.sleep(1)
connection.commit()
connection.close()
GPIO.cleanup()
