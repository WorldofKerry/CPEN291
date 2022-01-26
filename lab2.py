# student name: Kerry Wang
# student number: 82054420

# covid simple dashboard app

# imports
from ast import Str
from doctest import master
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from covid import Covid

from tkinter import *

import matplotlib
matplotlib.use("TkAgg")


def getMasterCovidData() -> list:
    """ this function is called once to get the master data for 
        this application; 
        all data used in this application is derived from data 
        returned by this function
    """
    covid = Covid()  # instantiate
    masterData = covid.get_data()

    # Sudo-random data for active and recovered
    for data in masterData:
        if (data['active'] is None):
            data['active'] = (data['confirmed'] + 2 *
                              data['deaths'])/2*(data['deaths'] % 7 + 1)
        if (data['recovered'] is None):
            data['recovered'] = (2*data['confirmed'] +
                                 data['deaths'])/2*(data['confirmed'] % 7 + 1)
    return masterData


def getConfirmed(data1: list) -> list:
    """ this function uses the masterdata data1 and returns a 
        list of (country, confirmed) data
    """
    confirmed = []
    for i in data1:
        confirmed.append((i["country"], i["confirmed"]))
    #print("DEBUG: confirmed is ", confirmed)
    return confirmed


def getTopCountry(masterData: list, selection: str) -> list:
    """ this function sues the masterdata selection 
    and returns a list of (country, value) in [selection] covid cases
    """
    return sorted(masterData, key=lambda x: x[selection], reverse=True)


def plotTopCountries(selection):
    """ a callback function for the button;
        plots a histogram of the top 10 confirmed cases 
    """
    global canvas, masterData, plotted    
    fig = Figure(figsize=(8, 5))
    plot1 = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=window)
    top10 = getTopCountry(masterData=masterData, selection=selection)
    x = [top10[i]['country'] for i in range(10)]
    y = [top10[i][selection] for i in range(10)]
    plot1.bar(x, y)

    for tick in plot1.get_xticklabels():  # rotate the text slightly
        tick.set_rotation(15)
    clear()
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, columnspan=4)
    plotted = True


def plotCountry(selection):
    """ a callback for the plot country data button"""    
    data = dict(
        list(filter(lambda x: x['country'] == selection, countryData))[0])
    global plotted, canvas
    fig = Figure(figsize=(8, 5))
    plot1 = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=window)
    # print("DEBUG: data", data)
    # if (data['active'] is None):
    #     data['active'] = (data['confirmed'] + 2*data['deaths']
    #                       )/2*(data['deaths'] % 7 + 1)
    # if (data['recovered'] is None):
    #     data['recovered'] = (2*data['confirmed'] +
    #                          data['deaths'])/2*(data['confirmed'] % 7 + 1)

    x = ["Confirmed", "Active", "Deaths", "Recovered"]
    y = [data['confirmed'], data['active'], data['deaths'], data['recovered']]
    plot1.bar(x, y)

    for tick in plot1.get_xticklabels():  # rotate the text slightly
        tick.set_rotation(15)
    clear()
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, columnspan=4)
    plotted = True


def clear():
    """ a callback for the Clear button """
    global plotted, canvas
    if plotted:
        canvas.get_tk_widget().destroy()
        plotted = False


# program starts here
# get masterData
masterData = getMasterCovidData()
#print("DEBUG: type(masterData) is", type(masterData))
# print(masterData)
confirmed = getConfirmed(masterData)
#print("DEBUG: type(confirmed) is", type(confirmed))
countryData = masterData[:10]
countryNames = list(map(lambda x: x['country'], countryData))

# instantiate the main window
window = Tk()
window.geometry("1000x700")

window.title("Covid Data Visualization")
window.columnconfigure(4, {'minsize': 40})

plotted = False

plot_label_string = StringVar()
plot_label_string.set("Plot Top 10 Countries for:")
plot_label = Label(master=window, textvariable=plot_label_string).grid(
    row=0, column=0)

options = ['confirmed', 'active', 'deaths', 'recovered']
variable = StringVar()
variable.set(options[0])
listboxCountryNames = OptionMenu(
    window, variable, *options, command=plotTopCountries).grid(row=0, column=1, sticky=W)

country_label_string = StringVar()
country_label_string.set("Country's Data:")
country_label = Label(master=window, textvariable=country_label_string).grid(
    row=0, column=2, sticky=W)

variable = StringVar()
variable.set(countryNames[0])
listboxCountryNames = OptionMenu(
    window, variable, *countryNames, command=plotCountry).grid(row=0, column=3, sticky=W)

plotTopCountries('confirmed')
window.mainloop()
