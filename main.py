import tkinter as tk
from clock import get_time, get_date
from weather import get_weather
from PIL import Image, ImageTk
import requests
from io import BytesIO

root = tk.Tk()
root.title("Smart Mirror")
root.configure(background='black')
root.attributes('-fullscreen', True)
root.bind("<Escape>", lambda e:root.destroy())
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)  # Top: Weather
root.grid_rowconfigure(1, weight=2)  # Middle: Time
root.grid_rowconfigure(2, weight=1)  # Bottom: Date


weather_frame = tk.Frame(root, bg='black')
weather_frame.grid(row = 0, column =1, padx = 20, pady = 20, sticky= 'ne')

# Time centered
time_label = tk.Label(root, font=('Helvetica', 80), fg='white', bg='black')
time_label.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky='nsew')

# Date top-right
date_label = tk.Label(root, font=('Helvetica', 40), fg='white', bg='black')
date_label.grid(row=0, column=0, padx=20, pady=10, sticky='nw')

#Weather Icon
weather_icon_label = tk.Label(weather_frame, bg='black')
weather_icon_label.pack(side='left', padx=(0, 10))

# Weather top-right
weather_label = tk.Label(weather_frame, font=('Helvetica', 30), fg='white', bg='black')
weather_label.pack(side='left')

def update_time():
    time_label.config(text=get_time())
    date_label.config(text=get_date())
    
    root.after(1000, update_time)

def update_weather():
    weather_text, icon_url = get_weather()
    weather_label.config(text=weather_text)

    if icon_url:
        try:
            response = requests.get(icon_url)
            image_data = Image.open(BytesIO(response.content)).resize((50, 50))
            weather_icon = ImageTk.PhotoImage(image_data)

            # Keep a reference or Tkinter will garbage collect it
            weather_icon_label.image = weather_icon
            weather_icon_label.config(image=weather_icon)

        except Exception as e:
            print(f"Error loading weather icon: {e}")

    root.after(600000, update_weather)



update_time()
update_weather()
root.mainloop()