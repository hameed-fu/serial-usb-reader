# main.py

import serial
import time
import random

USE_TEST_MODE = False

try:
    
    ser = serial.Serial(port='COM4', baudrate=11200, timeout=1)
    print("Listening on", ser.port)
except serial.SerialException:
    print("⚠️ No USB device detected on COM4. Running in TEST MODE.")
    USE_TEST_MODE = True

try:
    while True:
        if USE_TEST_MODE:
           
            test_data = f"Simulated Value: {random.randint(0, 100)}"
            print("Received:", test_data)
            time.sleep(2)
        else:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                print("Received:", line)
except KeyboardInterrupt:
    print("🛑 Stopped by user")
finally:
    if not USE_TEST_MODE and ser.is_open:
        ser.close()
        print("🔌 Serial port closed")
