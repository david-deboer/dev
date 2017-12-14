#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2017 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""Handling weather data.

"""
from __future__ import absolute_import, division, print_function
from astropy.time import Time
import numpy as np
import matplotlib.pyplot as plt


def plot(w='all'):
    weather_handling = Handling()
    weather_handling.plot_weather(w)


def data(w):
    weather_handling = Handling()
    x, y = weather_handling.data(w)
    return x, y


class Handling:
    wx_list = ['humidity', 'pressure', 'rain', 'temperature', 'wind_direction', 'wind_speed', 'wind_gust']

    def __init__(self):
        """
        This is a class to take various actions with the weather data in the database.
        """
        self.wx = None

    def data(self, wvar):
        data = np.loadtxt(wvar + '.txt')
        aptimes = Time(data[:, 0], format='gps').datetime
        w = data[:, 1]
        return aptimes, w

    def plot_weather(self, wx='all'):
        if isinstance(wx, str):
            if wx == 'all':
                wx = self.wx_list
            elif wx in self.wx_list:
                wx = [wx]
            else:
                print("Invalid wx variable request: {}".format(str(wx)))
                return
        for wvar in wx:
            data = np.loadtxt(wvar + '.txt')
            aptimes = Time(data[:, 0], format='gps').datetime
            plt.figure(wvar, figsize=(8, 5), tight_layout=True)
            plt.plot(aptimes, data[:, 1])
            plt.xticks(rotation=30, ha='right')
            plt.minorticks_on()
            plt.grid()
        plt.show()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--variables', help="csv-list of variable names or 'all'", default='all')
    args = parser.parse_args()
    if args.variables.lower() != 'all':
        args.variables = args.variables.split(',')
    W = Handling()
    W.plot_weather(args.variables)
