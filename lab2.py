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


class CovidGui:
    def __init__(self):
        # get masterData
        self.masterData = self.getMasterCovidData()
        #print("DEBUG: type(masterData) is", type(masterData))
        # print(masterData)
        self.confirmed = self.getConfirmed(self.masterData)
        #print("DEBUG: type(confirmed) is", type(confirmed))
        self.countryData = self.masterData[:10]
        countryNames = list(map(lambda x: x['country'], self.countryData))

        # instantiate the main window
        self.window = Tk()
        self.window.geometry("900x600")

        self.window.title("Covid Data Visualization")
        self.window.columnconfigure(4, {'minsize': 40})

        self.plotted = False

        plot_label_string = StringVar()
        plot_label_string.set("Plot Top 10 Countries for:")
        self.plot_label = Label(master=self.window, textvariable=plot_label_string).grid(
            row=0, column=0)

        options = ['confirmed', 'active', 'deaths', 'recovered']
        variable = StringVar()
        variable.set(options[0])
        self.listboxCountryNames = OptionMenu(
            self.window, variable, *options, command=self.plotTopCountries).grid(row=0, column=1, sticky=W)

        country_label_string = StringVar()
        country_label_string.set("Country's Data:")
        self.country_label = Label(master=self.window, textvariable=country_label_string).grid(
            row=0, column=2, sticky=W)

        variable = StringVar()
        variable.set(countryNames[0])
        self.listboxCountryNames = OptionMenu(
            self.window, variable, *countryNames, command=self.plotCountry).grid(row=0, column=3, sticky=W)

        self.plotTopCountries('confirmed')
        self.window.mainloop()

    def getMasterCovidData(self) -> list:
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
                                  data['deaths'])/2*(data['deaths'] % 3 + 1)
            if (data['recovered'] is None):
                data['recovered'] = (2*data['confirmed'] +
                                     data['deaths'])/2*(data['confirmed'] % 3 + 1)
        return masterData

    def getConfirmed(self, data1: list) -> list:
        """ this function uses the masterdata data1 and returns a 
            list of (country, confirmed) data
        """
        confirmed = []
        for i in data1:
            confirmed.append((i["country"], i["confirmed"]))
        #print("DEBUG: confirmed is ", confirmed)
        return confirmed

    def getTopCountry(self, selection: str) -> list:
        """ this function sues the masterdata selection 
            and returns a list of (country, value) in [selection] covid cases; 
            also replaces instead of "United Kingdom" with "UK" 
        """
        data = sorted(self.masterData,
                      key=lambda x: x[selection], reverse=True)
        for element in data:
            if (element['country'] == 'United Kingdom'):
                element['country'] = 'UK'
        return data

    def plotTopCountries(self, selection):
        """ a callback function for the button;
            plots a histogram of the top 10 confirmed cases 
        """
        fig = Figure(figsize=(8, 5))
        plot1 = fig.add_subplot(111)
        top10 = self.getTopCountry(selection=selection)
        x = [top10[i]['country'] for i in range(10)]
        y = [top10[i][selection] for i in range(10)]
        plot1.bar(x, y)
        for tick in plot1.get_xticklabels():  # rotate the text slightly
            tick.set_rotation(15)
        self.clear()
        self.canvas = FigureCanvasTkAgg(fig, master=self.window)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, columnspan=4)
        self.plotted = True

    def plotCountry(self, selection):
        """ a callback for the plot country data button"""
        data = dict(
            list(filter(lambda x: x['country'] == selection, self.countryData))[0])
        global plotted, canvas
        fig = Figure(figsize=(8, 5))
        plot1 = fig.add_subplot(111)
        x = ["Confirmed", "Active", "Deaths", "Recovered"]
        y = [data['confirmed'], data['active'],
             data['deaths'], data['recovered']]
        plot1.bar(x, y)
        for tick in plot1.get_xticklabels():  # rotate the text slightly
            tick.set_rotation(15)
        self.clear()
        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, columnspan=4)
        plotted = True

    def clear(self):
        """ a callback for the Clear button """
        if self.plotted:
            self.canvas.get_tk_widget().destroy()
            self.plotted = False


if __name__ == "__main__":
    CovidGui()
