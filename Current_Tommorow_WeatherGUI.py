import tkinter as tk
import requests
from tkinter import ttk, messagebox
from datetime import datetime as dt2
import datetime
import calendar
import time
from tkinter.ttk import Combobox


#    Because the classic ttk Combobox does not take a dictionary for values.
class NewCombobox(Combobox):
    
    def __init__(self, master, dictionary, *args, **kwargs):
        Combobox.__init__(self, master,
                          values=sorted(list(dictionary.keys())),
                          *args, **kwargs)
        self.dictionary = dictionary

    def get(self):
        if Combobox.get(self) == '':
            return ''
        else:
            return self.dictionary[Combobox.get(self)]

# TK Functions

def increase_window_width():
    win.minsize(width=300, height=1)
    win.resizable(0, 0)

def _about():
    mb = messagebox.showinfo(message='''Script Created By Ben Zikri
        Version 1.02''', title='About')

def _quit():
    win.quit()
    win.destroy()
    exit()

# Create TK instance

win = tk.Tk()
win.title('Weather Checker')

# Creating Menu Bar

menuBar = tk.Menu()
win.config(menu=menuBar)

# Creating menu items

fileMenu = tk.Menu(menuBar, tearoff=0)
fileMenu.add_command(label='New')
fileMenu.add_separator()
fileMenu.add_command(label='Exit', command=_quit)
menuBar.add_cascade(label='File', menu=fileMenu)

helpMenu = tk.Menu(menuBar, tearoff=0)
helpMenu.add_command(label='About', command=_about)
menuBar.add_cascade(label='Help', menu=helpMenu)

# Creating tabs

tabControl = ttk.Notebook(win)
tab1 = tk.Frame(tabControl)
tabControl.add(tab1, text='Current Observations')
tab2 = tk.Frame(tabControl)
tabControl.add(tab2, text='Tomorrow Observations')
tabControl.pack(expand=1, fill='both')


####### Tab 1-current weather status

# Creating labels

weather_condition_frame = ttk.Labelframe(
    tab1, text='Current Weather Condition')

weather_condition_frame.grid(column=0, row=1, padx=8, pady=4)
weather_cities_frame = ttk.Labelframe(tab1, text='Latest Observation For ')
weather_cities_frame.grid(column=0, row=0, padx=8, pady=4)
ttk.Label(weather_cities_frame, text='Location:        ').grid(column=0, row=0)

values = {'Jerusalem': 'Jerusalem', 'Kfar Saba': 'Kfar+Saba', 'Beer Sheva': 'Beersheba'}

city = tk.StringVar()
citySelected = NewCombobox(weather_cities_frame, values, width=12, textvariable=city)
citySelected.grid(column=1, row=0)
citySelected.current(0)

# Get city from Combobox then call get weather function which city parameter

def _get_city():
    selected_city = citySelected.get()
    get_weather_data(selected_city)
    
# Make a button for getting the data to GUI

get_weather_btn = ttk.Button(weather_cities_frame, text='Get Weather', command=_get_city).grid(column=2, row=0)

# Making entries for the values in the GUI

max_width = max([len(x) for x in citySelected['values']])
new_width = max_width + 2
citySelected.config(width=new_width)

ENTRY_WIDTH = 24

ttk.Label(weather_condition_frame, text='Last Update: ').grid(column=0, row=1, sticky='E')
updated = tk.StringVar()
updatedEntry = ttk.Entry(weather_condition_frame, width=ENTRY_WIDTH, textvariable=updated, state='readonly')
updatedEntry.grid(column=1, row=1, sticky='W')

ttk.Label(weather_condition_frame, text='Weather: ').grid(column=0, row=2, sticky='E')
weather = tk.StringVar()
updatedEntry = ttk.Entry(weather_condition_frame, width=ENTRY_WIDTH, textvariable=weather, state='readonly')
updatedEntry.grid(column=1, row=2, sticky='W')

ttk.Label(weather_condition_frame, text='Temprature: ').grid(column=0, row=3, sticky='E')
temp = tk.StringVar()
updatedEntry = ttk.Entry(weather_condition_frame, width=ENTRY_WIDTH, textvariable=temp, state='readonly')
updatedEntry.grid(column=1, row=3, sticky='W')

ttk.Label(weather_condition_frame, text='Minimun Temprature: ').grid(column=0, row=4, sticky='E')
min_temp = tk.StringVar()
updatedEntry = ttk.Entry(weather_condition_frame, width=ENTRY_WIDTH, textvariable=min_temp, state='readonly')
updatedEntry.grid(column=1, row=4, sticky='W')

ttk.Label(weather_condition_frame, text='Maximum Temprature: ').grid(column=0, row=5, sticky='E')
max_temp = tk.StringVar()
updatedEntry = ttk.Entry(weather_condition_frame, width=ENTRY_WIDTH, textvariable=max_temp, state='readonly')
updatedEntry.grid(column=1, row=5, sticky='W')

ttk.Label(weather_condition_frame, text='Humidity: ').grid(column=0, row=6, sticky='E')
humi = tk.StringVar()
updatedEntry = ttk.Entry(weather_condition_frame, width=ENTRY_WIDTH, textvariable=humi, state='readonly')
updatedEntry.grid(column=1, row=6, sticky='W')

for child in weather_condition_frame.winfo_children():
    child.grid_configure(padx=4, pady=1)


# next we update the Entry widget with this data

def get_weather_data(selected_city):

    now = dt2.now()
    updated_data = now.strftime("%H:%M     %d/%m/%Y")
    updated.set(updated_data)

    url_general = 'http://api.openweathermap.org/data/2.5/weather?q={},il&appid=ec7767086a74e545346c22459773fd7c&units=metric'
    url = url_general.format(selected_city)
    
    res = requests.get(url)
    data = res.json()

    weather_now = data['weather'][0]['description']
    temprature_now = data['main']['temp']
    humi_now = data['main']['humidity']
    min_temp_now = data['main']['temp_min']
    max_temp_now = data['main']['temp_max']
    weather.set(weather_now)
    temp.set(temprature_now)
    humi.set(humi_now)
    min_temp.set(min_temp_now)
    max_temp.set(max_temp_now)


####### Tab 2-forcasting tomorrow weather at 12:00 am.

weather_condition_frame2 = ttk.Labelframe(
    tab2, text='Tomorrow Weather Condition')

weather_condition_frame2.grid(column=0, row=1, padx=8, pady=4)

weather_cities_frame2 = ttk.Labelframe(tab2, text='Latest Observation For ')
weather_cities_frame2.grid(column=0, row=0, padx=8, pady=4)
ttk.Label(weather_cities_frame2, text='Location:        ').grid(column=0, row=0)

values = {'Jerusalem': 'Jerusalem', 'Kfar Saba': 'Kfar+Saba', 'Beer Sheva': 'Beersheba'}

city = tk.StringVar()
citySelected2 = NewCombobox(weather_cities_frame2, values, width=12, textvariable=city)
citySelected2.grid(column=1, row=0)
citySelected2.current(1)


def _get_city2():
    selected_city = citySelected2.get()
    get_tom_weather_data(selected_city)
    # populate_gui_from_dict()


get_weather_btn2 = ttk.Button(weather_cities_frame2, text='Get Weather', command=_get_city2).grid(column=2, row=0)


max_width = max([len(x) for x in citySelected['values']])
new_width = max_width + 2
citySelected.config(width=new_width)

ENTRY_WIDTH = 24


ttk.Label(weather_condition_frame2, text='Forecasted for: ').grid(column=0, row=1, sticky='E')
updated2 = tk.StringVar()
updatedEntry = ttk.Entry(weather_condition_frame2, width=ENTRY_WIDTH, textvariable=updated2, state='readonly')
updatedEntry.grid(column=1, row=1, sticky='W')

ttk.Label(weather_condition_frame2, text='Weather: ').grid(column=0, row=2, sticky='E')
weather2 = tk.StringVar()
updatedEntry = ttk.Entry(weather_condition_frame2, width=ENTRY_WIDTH, textvariable=weather2, state='readonly')
updatedEntry.grid(column=1, row=2, sticky='W')

ttk.Label(weather_condition_frame2, text='Temprature: ').grid(column=0, row=3, sticky='E')
temp2 = tk.StringVar()
updatedEntry = ttk.Entry(weather_condition_frame2, width=ENTRY_WIDTH, textvariable=temp2, state='readonly')
updatedEntry.grid(column=1, row=3, sticky='W')

ttk.Label(weather_condition_frame2, text='Minimun Temprature: ').grid(column=0, row=4, sticky='E')
min_temp2 = tk.StringVar()
updatedEntry = ttk.Entry(weather_condition_frame2, width=ENTRY_WIDTH, textvariable=min_temp2, state='readonly')
updatedEntry.grid(column=1, row=4, sticky='W')

ttk.Label(weather_condition_frame2, text='Maximum Temprature: ').grid(column=0, row=5, sticky='E')
max_temp2 = tk.StringVar()
updatedEntry = ttk.Entry(weather_condition_frame2, width=ENTRY_WIDTH, textvariable=max_temp2, state='readonly')
updatedEntry.grid(column=1, row=5, sticky='W')

ttk.Label(weather_condition_frame2, text='Humidity: ').grid(column=0, row=6, sticky='E')
humi2 = tk.StringVar()
updatedEntry = ttk.Entry(weather_condition_frame2, width=ENTRY_WIDTH, textvariable=humi2, state='readonly')
updatedEntry.grid(column=1, row=6, sticky='W')

for child in weather_condition_frame2.winfo_children():
    child.grid_configure(padx=4, pady=1)


def get_tom_weather_data(selected_city):

    tommorow_date = datetime.date.today() + datetime.timedelta(days=1)
    timestampStr = tommorow_date.strftime("%Y-%m-%d")
    tommorow_date_unix = calendar.timegm(time.strptime(timestampStr, '%Y-%m-%d')) + 43200

    api = 'ec7767086a74e545346c22459773fd7c&units=metric'
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={selected_city}&appid={api}'
  
    res = requests.get(url)
    data = res.json()

    for i in range(39):
        if data['list'][i]['dt'] == tommorow_date_unix:
            temprature_tom = data['list'][i]['main']['temp']
            weather_tom = data['list'][i]['weather'][0]['main']
            min_temp_tom = data['list'][i]['main']['temp_min']
            max_temp_tom = data['list'][i]['main']['temp_max']
            humi_tom = data['list'][i]['main']['humidity']
            break

    updated2.set(tommorow_date.strftime("12:00     %d/%m/%Y"))
    weather2.set(weather_tom)
    temp2.set(temprature_tom)
    humi2.set(humi_tom)
    min_temp2.set(min_temp_tom)
    max_temp2.set(max_temp_tom)



# Start GUI
win.mainloop()
