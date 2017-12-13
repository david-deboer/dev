#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2017 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""Handling weather data.

"""
from __future__ import absolute_import, division, print_function
from astropy.time import Time
from hera_mc import mc, weather


class Handling:

    def __init__(self, session=None):
        """
        This is a class to take various actions with the weather data in the database.
        """
        if session is None:
            db = mc.connect_to_mc_db(None)
            self.session = db.sessionmaker()
        else:
            self.session = session
        self.wx = None

    def read_weather_files(self, wx=['humidity', 'pressure', 'rain', 'temperature', 'wind_direction', 'wind_speed', 'wind_gust'], path='.'):
        """
        Reads in the weather files as written by self.write_weather_files.

        Parameters:
        -----------
        wx:  variables to be read.
        path:  path to read files.  Defaults to current
        """
        import os.path
        self.wx = {}
        path = os.path.expanduser(path)
        for wvar in wx:
            self.wx[wvar] = {}
            with open(os.path.join(path, (wvar + '.txt')), 'r') as f:
                for data in f:
                    d = data.split()
                    self.wx[wvar][int(d[0])] = float(d[1])

    def plot_weather(self, wx=['humidity', 'pressure', 'rain', 'temperature', 'wind_direction', 'wind_speed', 'wind_gust'], path='.'):
        import matplotlib.pyplot as plt
        self.read_weather_files(wx=wx, path=path)
        for wvar, v in self.wx.iteritems():
            times = sorted(v.keys())
            x = []
            y = []
            for t in times:
                a = Time(t, format='gps').datetime
                # a = t
                x.append(a)
                y.append(v[t])
            plt.figure(wvar)
            plt.plot(x, y)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--write-data-files', dest='write_data_files', help="Write data files from dictionary.")
    parser.add_argument('-r', '--read-data-from-table', dest='read_data_from_table', help="Read data from table.")
    parser.add_argument('-f', '--read-data-from-files', dest='read_data_from_files', help="Read data from files.")
