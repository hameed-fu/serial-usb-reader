# main.py (GUI version)

import serial
import time
import random
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

USE_TEST_MODE = False

def read_serial():
    global ser, USE_TEST_MODE
    try:
        ser = serial.Serial(port='COM4', baudrate=11200, timeout=1)
        append_text(f"✅ Listening on {ser.port}")
    except serial.SerialException:
        append_text("⚠️ No USB device detected on COM4. Running in TEST MODE.")
        USE_TEST_MODE = True

    while running:
        if USE_TEST_MODE:
            test_data = f"Simulated Value: {random.randint(0, 100)}"
            append_text(f"Received: {test_data}")
            time.sleep(2)
        else:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                append_text(f"Received: {line}")

def append_text(text):
    output_box.insert(tk.END, text + "\n")
    output_box.see(tk.END)

def start_reading():
    global running, reader_thread
    running = True
    reader_thread = threading.Thread(target=read_serial, daemon=True)
    reader_thread.start()

def stop_reading():
    global running
    running = False
    append_text("🛑 Stopped by user")
    try:
        if not USE_TEST_MODE and ser.is_open:
            ser.close()
            append_text("🔌 Serial port closed")
    except:
        pass

# GUI
root = tk.Tk()
root.title("USB Serial Reader")

output_box = ScrolledText(root, width=60, height=20)
output_box.pack(padx=10, pady=10)

button_frame = tk.Frame(root)
button_frame.pack()

start_btn = tk.Button(button_frame, text="Start", command=start_reading)
start_btn.pack(side=tk.LEFT, padx=5)

stop_btn = tk.Button(button_frame, text="Stop", command=stop_reading)
stop_btn.pack(side=tk.LEFT, padx=5)

root.protocol("WM_DELETE_WINDOW", lambda: [stop_reading(), root.destroy()])
root.mainloop()
