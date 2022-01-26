# student name: Kerry Wang
# student number: 82054420

# covid simple dashboard app

# imports
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
    data = covid.get_data()
    return data


def getConfirmed(data1: list) -> list:
    """ this function uses the masterdata data1 and returns a 
        list of (country, confirmed) data
    """
    confirmed = []
    for i in data1:
        confirmed.append((i["country"], i["confirmed"]))
    #print("DEBUG: confirmed is ", confirmed)
    return confirmed


def plotConfirmed():
    """ a callback function for the button;
        plots a histogram of the top 10 confirmed cases 
    """
    global canvas
    clear()
    fig = Figure(figsize=(8, 5))
    plot1 = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=window)

    top10 = [confirmed[i] for i in range(10)]
    # print("DEBUG: top10", top10)
    x = [top10[i][0] for i in range(10)]
    y = [top10[i][1] for i in range(10)]
    plot1.bar(x, y)

    for tick in plot1.get_xticklabels():  # rotate the text slightly
        tick.set_rotation(15)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, columnspan=4)
    plotted = True


def clear():
    """ a callback for the Clear button """
    global plotted, canvas
    if plotted:
        canvas.get_tk_widget().destroy()
        plotted = False
    global text
    text.destroy()


def plotCountry(selection):
    """ a callback for the plot country data button"""
    clear()
    data = dict(
        list(filter(lambda x: x['country'] == selection, countryData))[0])
    # dataString = "Confirmed: " + str(data['confirmed']) + "; Active: " + str(
    #     data['active']) + "; Deaths: " + str(data['deaths']) + "; Recovered: " + str(data['recovered'])
    # text = Text(window, width=len(dataString), height=1)
    # text.insert(INSERT, dataString)
    # text.grid(row=1, columnspan=3)

    global plotted, canvas
    if plotted:
        return
    fig = Figure(figsize=(8, 5))
    plot1 = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=window)
    # print("DEBUG: data", data)
    if (data['active'] is None): 
        data['active'] = (data['confirmed'] + 2*data['deaths'])/2*(data['deaths'] % 7 + 1)
    if (data['recovered'] is None): 
        data['recovered'] = (2*data['confirmed'] + data['deaths'])/2*(data['confirmed'] % 7 + 1)

    x = ["Confirmed", "Active", "Deaths", "Recovered"]
    y = [data['confirmed'], data['active'], data['deaths'], data['recovered']]
    plot1.bar(x, y)

    for tick in plot1.get_xticklabels():  # rotate the text slightly
        tick.set_rotation(15)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, columnspan=4)
    plotted = True



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

plotted = False

plot_label_string = StringVar()
plot_label_string.set("Plot Top 10 Countries for:")
plot_label = Label(master=window, textvariable=plot_label_string).grid(row=0, column=0)

plot_button = Button(master=window,
                     command=lambda: plotConfirmed(),
                     height=2,
                     width=15,
                     text="Plot").grid(row=0, column=1, sticky=W)

# clear_button = Button(master=window,
#                       command=lambda: clear(),
#                       height=2,
#                       width=10,
#                       text="Clear").grid(row=0, column=2, sticky='WW')

text = Text()

country_label_string = StringVar()
country_label_string.set("Country's Data:")
country_label = Label(master=window, textvariable=country_label_string).grid(row=0, column=2, sticky=W)

variable = StringVar()
variable.set(countryNames[0])
listboxCountryNames = OptionMenu(
    window, variable, *countryNames, command=plotCountry).grid(row=0, column=3, sticky=W)
plotConfirmed()
window.mainloop()

# Top Countries for: SelectMenu; Plot Countries: SelectMenu
