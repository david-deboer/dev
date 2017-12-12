# -*- mode: python; coding: utf-8 -*-
# Copyright 2017 the HERA Collaboration
# Licensed under the 2-clause BSD license.

"""
Eventually move this to hera_mc/hera_mc/weather.py

"""
from __future__ import absolute_import, division, print_function
from tabulate import tabulate
from astropy.time import Time

from hera_mc import mc, cm_utils
from hera_mc import weather as W


class Handling:

    def __init__(self, session=None):
        """

        """
        if session is None:
            db = mc.connect_to_mc_db(None)
            self.session = db.sessionmaker()
        else:
            self.session = session
        self.wx = None

    def read_weather_table(self):
        """
        Get next connected part going the given direction.
        """

        self.wx = {}
        for wl in self.session.query(W.WeatherData):
            if wl.variable not in self.wx.keys():
                self.wx[wl.variable] = {}
            self.wx[wl.variable][wl.time] = wl.value

    def get_weather(self):
        if self.wx is None:
            self.read_weather_table()
        return self.wx

    def write_weather_files(self):
        if self.wx is None:
            self.read_weather_table()
        for k, v in self.wx.iteritems():
            with open(k + '.txt', 'w') as f:
                times = sorted(v.keys())
                for t in times:
                    s = '{}\t{}\n'.format(t, v[t])
                    f.write(s)
