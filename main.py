import tkinter as tk
import pyaudio
import numpy as np
import random
import math

colors = [
    '#f1c40f',
    '#e67e22',
    '#c0392b',
    '#3498db',
    '#8e44ad'
]

# Set up audio stream
chunk = 1024
format = pyaudio.paInt16
rate = 44100
pa = pyaudio.PyAudio()
stream = pa.open(format=format, rate=rate, channels=1, input=True, frames_per_buffer=chunk)

# Set up the Tkinter window
root = tk.Tk()
root.title("Audio Shapes")
root.geometry("800x600")  # Size of the window
root.attributes('-topmost', True)  # Make sure window is on top
root.attributes('-transparentcolor', 'white')  # Set transparent color

# Create a canvas for drawing
canvas = tk.Canvas(root, bg='white')
canvas.pack(fill=tk.BOTH, expand=True)

# Function to draw shapes based on audio data
def draw_shapes(data):
    # Clear previous shapes
    canvas.delete("all")
    lines_len = 50
    angle = 0
    color = random.choice(colors)
    for i in range(lines_len):
        start_x = 400
        start_y = 300
        audio_level = np.max(data) - np.min(data)
        #print(audio_level)
        rad = math.radians(angle + (lines_len / 360) * i )
        end_x = (start_x + math.cos(rad) * audio_level)
        end_y = (start_y + math.sin(rad) * audio_level)
        canvas.create_line((start_x, start_y, end_x, end_y), 
                           fill = color, width=5)
        angle += 10




# Continuously capture audio and draw shapes
while True:
    try:
        audio_data = np.frombuffer(stream.read(chunk), dtype=np.int16)
        draw_shapes(audio_data)
        root.update_idletasks()
        root.update()
    except tk.TclError:
        # Handle the exception when the window is closed
        break

#Clean up on exit
stream.stop_stream()
stream.close()
pa.terminate()
root.destroy()
