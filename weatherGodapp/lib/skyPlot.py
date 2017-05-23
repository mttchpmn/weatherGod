# TODO - Implement zoomed chart class
# TODO - Fix Bug where it looks like altitude is not displaying accurately on scale
# TODO - Refactor to use 'fig = plt.figure()'

import numpy as np
import matplotlib.pyplot as plt

from skyPy import Sounding
from pprint import pprint

############################################################################################################


class Tephigram(object):
    def __init__(self, station, index):
        """Retrieve and transcode raw Radiosonde data into dictionary;
        then strip values from dictionary into lists to be plotted.
        NB: PARENT CLASS - Do NOT instantiate directly."""
        sounding = Sounding(station, index)
        self.data = sounding.data
        valid_from = sounding.valid_from

        self.alt = self.strip_values('altitude', self.data)
        self.temp = self.strip_values('temp', self.data)
        self.dp = self.strip_values('dewpoint', self.data)
        self.pres = self.strip_values('pressure', self.data)

        self.fig, self.ax1 = plt.subplots()
        self.ax2 = self.ax1.twinx()

        self.ax1.set_xlabel('Temperature (Deg C')
        self.ax1.set_ylabel('Pressure (mBar)')
        self.ax2.set_ylabel('Altitude (m)')
        t = 'Lapse Rate - Valid: {}'.format(valid_from)
        plt.title(t)

        plt.grid(b=True, which='major', axis='y', color='g', linestyle='--')

    ####################################################

    @staticmethod
    def strip_values(key, data):
        l = []
        for i in data:
            value = i.get(key)
            l.append(value)
        return l

    ####################################################

    @staticmethod
    def show():
        plt.show()

############################################################################################################


class Zoom(Tephigram):
    def __init__(self, station, index):
        super(Zoom, self).__init__(station, index)

        i = self.zoom_index(self.pres)
        self.pres_zoom = self.pres[:i:]
        self.temp_zoom = self.temp[:i:]
        self.dp_zoom = self.dp[:i:]

        self.ax1.axis([-20, 20, 1050, 800])
        self.ax2.axis([-20, 20, 0, 3000])

        plt.yticks([50, 100, 150, 300, 500, 750,  1000, 1250, 1500, 2000, 3000])
        plt.xticks([-20, -18, -16, -14, -12, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1,
                    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20])

        self.ax1.plot(self.dp_zoom, self.pres_zoom, '-b', label='Dew Point')
        self.ax1.plot(self.temp_zoom, self.pres_zoom, '-r', label='Temperature')
        #  self.ax2.plot(self.temp, self.alt, '-r')
        self.ax1.legend(loc='upper right')

    ####################################################

    @staticmethod
    def zoom_index(l):
        for i in l:
            if int(i) <= 800:
                end_index = l.index(i) + 1
                break
        return end_index

############################################################################################################


class Full(Tephigram):
    def __init__(self, station, index):
        super(Full, self).__init__(station, index)

        self.ax1.axis([-60, 60, 1050, 250])
        self.ax2.axis([-60, 60, 0, 10000])

        plt.yticks([100, 500, 1000, 1500, 2000, 3000, 5000, 7500, 10000])
        plt.xticks([-60, -50, -40, -30, -20, -15, -10, -5, 0, 5, 10, 15, 20, 30, 40, 50, 60])

        self.ax1.plot(self.dp, self.pres, '-b', label='Dew Point')
        self.ax1.plot(self.temp, self.pres, '-r', label='Temperature')
        #  self.ax2.plot(self.temp, self.alt, '-r')
        self.ax1.legend(loc='upper right')

############################################################################################################

test = Zoom('93844', 0)

test.show()
