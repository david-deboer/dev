# -*- mode: python; coding: utf-8 -*-
# Copyright 2017 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
Some extra local weather help

"""
from __future__ import absolute_import, division, print_function
from astropy.time import Time
import matplotlib.pyplot as plt
from hera_mc import weather

W = weather.Handling()


def plot_weather(path='.'):
    W.read_weather_files(path=path)
    for k, v in W.wx.iteritems():
        times = sorted(v.keys())
        x = []
        y = []
        for t in times:
            a = Time(t, format='gps').datetime
            # a = t
            x.append(a)
            y.append(v[t])
        plt.figure(k)
        plt.plot(x, y)
