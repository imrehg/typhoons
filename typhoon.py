#!/usr/bin/env python2
"""
Typhoon data log analysis for Soulik (2013) and Soudelor (2015)

Data recorded with a BMP085 breakout board + Arduino Nano + Raspberry Pi

Location of recording: near but not exactly 25.024179, 121.528492

The format of the two dataset is slightly different, as I used a
different version of the logger code for the two events.

The Soudelor data is in two files, as there was a short stop in
the recording, resumed later (can be concatenated).

Software required:
==================
Python (2.x series): https://www.python.org/downloads/
Numpy: http://www.numpy.org/
Matplotlib: http://matplotlib.org/

Links:
======
Typhoon Soulik: https://en.wikipedia.org/wiki/Typhoon_Soulik_(2013)
Typhoon Soudelor: https://en.wikipedia.org/wiki/Typhoon_Soudelor_(2015)
BMP085: https://www.adafruit.com/products/391
Arduino Nano: https://www.arduino.cc/en/Main/arduinoBoardNano
Raspberry Pi: https://www.raspberrypi.org/products/model-b/

License:
========
Software: MIT License
          http://opensource.org/licenses/MIT
Data: Open Data Commons Public Domain Dedication and License (PDDL)
      http://opendatacommons.org/licenses/pddl/

"""
from __future__ import division
import numpy
from matplotlib.dates import strpdate2num
import pylab as pl

def convertDate(dateData):
    """ Convert time data for plotting:
        seconds to hours
    """
    return dateData / 60 / 60

def convertPressure(pressureData):
    """ Convert pressure data for plotting:
        pascal to hectopascal
    """
    return pressureData / 100.0

if __name__ == '__main__':
    # Data drom Typhoon Soulik (2013)
    typhoon1file = "barolog_201307111346.csv"
    typhoon1 = numpy.loadtxt(typhoon1file, delimiter=',')
    mindateindex1 = numpy.argmin(typhoon1[:,2])  # find index of minimum atm. pressure
    t1date = typhoon1[:, 0]-typhoon1[mindateindex1, 0]
    t1pressure = typhoon1[:, 2]

    # Data from Typhoon Soudelor (2015), two parts
    typhoon2afile = "templog_20150807_190517.csv"
    typhoon2a = numpy.loadtxt(typhoon2afile, delimiter=',', converters={0:strpdate2num("%Y-%m-%d %H:%M:%S.%f")})
    typhoon2bfile = "templog_20150808_183532.csv"
    typhoon2b = numpy.loadtxt(typhoon2bfile, delimiter=',', converters={0:strpdate2num("%Y-%m-%d %H:%M:%S.%f")})
    typhoon2 = numpy.append(typhoon2a, typhoon2b, axis=0)
    mindateindex2 = numpy.argmin(typhoon2[:, 2])
    t2date = (typhoon2[:, 0]-typhoon2[mindateindex2, 0]) * 24 * 60 * 60
    t2pressure = typhoon2[:, 2]

    pl.figure(figsize=(12, 9))
    # Remove the plot frame lines. They are unnecessary chartjunk.
    ax = pl.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(True)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(True)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    ax.set_xlim([convertDate(t1date[0]), convertDate(t1date[-1])])

    ax.plot(convertDate(t1date),
            convertPressure(t1pressure),
            lw=1.5,
            color='black',
            label='Soulik (2013)\n[Eye passing almost directly above]'
    )
    ax.plot(convertDate(t2date),
            convertPressure(t2pressure),
            lw=1.5,
            color='blue',
            label='Soudelor (2015)\n[Eye passing about 70km away]'
    )
    pl.title('Atmospheric pressure during typhoon passage', fontsize=22)
    pl.xlabel('Time-delta from minimum atm. pressure (h)', fontsize=16)
    pl.ylabel('Atmospheric pressure (hPa)', fontsize=16)
    pl.legend(loc='lower left', fontsize=18)
    pl.grid(True)
    pl.savefig("Typhoon_Comparison.png", bbox_inches="tight");  
    pl.show()
