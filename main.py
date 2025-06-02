import tkinter as tk
import urllib.request
import requests
from clock import get_time, get_date
from weather import get_weather, get_forecast
from PIL import Image, ImageTk
from io import BytesIO
from calendar_events import get_today_events
from news import get_headlines


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
time_label.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky='n')

# Date top-right
date_label = tk.Label(root, font=('Helvetica', 40), fg='white', bg='black')
date_label.grid(row=0, column=0, padx=20, pady=10, sticky='nw')

#Weather Icon
weather_icon_label = tk.Label(weather_frame, bg='black')
weather_icon_label.pack(side='left', padx=(0, 10))

# Weather top-right
weather_label = tk.Label(weather_frame, font=('Helvetica', 30), fg='white', bg='black')
weather_label.pack(side='left')

# Get events
events = get_today_events()
event_text = "Today's Events:\n" + "\n".join(f"- {e}" for e in events)

events_label = tk.Label(root, text=event_text, font=('Helvetica', 24), fg='white', bg='black', justify='left', anchor='nw')
events_label.grid(row=4, column=0, padx=20, pady=(10, 10), sticky='nw')

#news from NPR
headlines = get_headlines()
headlines_text = "Top Headlines:\n" + "\n".join(f"• {h}" for h in headlines)

news_label = tk.Label(root, text=headlines_text, font=('Helvetica', 18), fg='white', bg='black', justify='left', anchor='ne')
news_label.grid(row=4, column=1, padx=20, pady=(10, 10), sticky='ne')

#update time every second
def update_time():
    time_label.config(text=get_time())
    date_label.config(text=get_date())
    
    root.after(1000, update_time)


#update weather and icon every 10 min to limit API
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

#create lists for forecast
forecast_labels = []
forecast_icons = []
forecast_images = []


# Container frame for forecast entries
forecast_frame = tk.Frame(root, bg='black')
forecast_frame.grid(row=1, column=1, sticky='ne', padx=20, pady=10)

for i in range(3):
    frame = tk.Frame(forecast_frame, bg='black')
    frame.pack(anchor='e', pady=(0 if i == 0 else 5))

    icon_label = tk.Label(frame, bg='black')
    icon_label.pack(side='left', padx=(0, 10))

    text_label = tk.Label(frame, font=('Helvetica', 20), fg='white', bg='black')
    text_label.pack(side='left')

    forecast_icons.append(icon_label)
    forecast_labels.append(text_label)


def update_forecast():
    forecasts = get_forecast()

    # Clear old image references
    forecast_images.clear()

    for i, (text, icon_url) in enumerate(forecasts):
        forecast_labels[i].config(text=text)

        if icon_url:
            try:
                with urllib.request.urlopen(icon_url) as u:
                    raw_data = u.read()
                img = Image.open(BytesIO(raw_data)).resize((50, 50))
                photo = ImageTk.PhotoImage(img)

                forecast_icons[i].config(image=photo)
                forecast_images.append(photo)  # Store it so it isn't garbage collected

            except Exception as e:
                print(f"Error loading forecast icon: {e}")

    root.after(600000, update_forecast)
 
update_time()
update_weather()
update_forecast()
root.mainloop()