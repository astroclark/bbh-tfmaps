#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Copyright (C) 2017-2017 James Clark <james.clark@ligo.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
tfmap.py

plots a time-frequency map of an arbitrary time series (contained in a
user-supplied ascii file) using a continuous wavelet transform
"""

from __future__ import division
import os,sys
import numpy as np

import cwt

from matplotlib import pyplot as pl

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def build_cwt(timeseries, timestamps, max_scale=128, mother_freq=4, Norm=True):

    delta_t = np.diff(timestamps)[0]
    sample_rate = 1./delta_t

    # Range of wavelet scales we're interested in
    scales = 1+np.arange(max_scale)

    # Construct the 'mother wavelet'; we'll begin using a Morlet wavelet
    # (sine-Gaussian) but we should/could investigate others
    mother_wavelet = cwt.Morlet(len_signal=len(timeseries), scales=scales,
            sampf=delta_t, f0=mother_freq)

    # Compute the CWT
    wavelet = cwt.cwt(timeseries, mother_wavelet)

    # Take the absolute values of coefficients 
    tfmap = np.abs(wavelet.coefs)

    # Normalise
    tfmap /= max(map(max,abs(wavelet.coefs)))

    # Determine frequency at each scale
    freqs = sample_rate * wavelet.motherwavelet.fc \
            / wavelet.motherwavelet.scales

    # Return a dictionary
    timefreq = dict()
    timefreq['analysed_data'] = timeseries
    timefreq['map'] = tfmap
    timefreq['times'] = timestamps
    timefreq['frequencies'] = freqs
    timefreq['scales'] = scales
    timefreq['mother_wavelet'] = mother_wavelet
    timefreq['image_shape'] = np.shape(tfmap)


    return timefreq

def plot_map(cwt_result, xlims, ylims):


    signal = cwt_result['analysed_data']
    Z = np.copy(cwt_result['map'])

    for c in xrange(np.shape(Z)[1]):
        Z[:,c] /= np.log10(np.sqrt(cwt_result['frequencies']) / 2)

    # Open the figure
    fig, ax_cont = pl.subplots(figsize=(10,5),nrows=2)

    #maxcol = 0.45*Z.max()
    maxcol = 0.8*Z.max()
    vmin, vmax = 0, maxcol
    collevs=np.linspace(vmin, vmax, 100)

    # Characteristic times
    tmax = cwt_result['times'][np.argmax(signal)]

    # --- CWT
    #c = ax_cont.contourf(cwt_result['times']-tmax, cwt_result['frequencies'], Z,
    #        levels=collevs, extend='both')
    c = ax_cont[0].pcolormesh(cwt_result['times']-tmax, cwt_result['frequencies'], Z)

    #p = ax_cont[1].plot(cwt_result['times']-tmax, cwt_result['analysed_data'])
    p1 = ax_cont[1].plot(cwt_result['times']-tmax, cwt_result['analysed_data'])
    p2 = ax_cont[1].plot(cwt_result['times']-tmax,
            abs(cwt_result['analysed_data']), linestyle='--')

    c.cmap.set_over('k')
    c.set_cmap('gnuplot2')

    #ax_cont.set_yscale('log')
    ax_cont[1].set_xlabel('Time')
    ax_cont[0].set_ylabel('Frequency')
    ax_cont[1].set_ylabel('Strain')
    ax_cont[0].set_ylim(ylims)
    ax_cont[0].set_xlim(xlims)
    ax_cont[1].set_xlim(xlims)

    return fig, ax_cont

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Load Data
#
#   strain = np.genfromtxt('samplewave.txt')
#   max_scale=1024
#   mother_freq=0.3
#   ylims=(0,0.5)
#   xlims=(-400,100)

strain = np.genfromtxt('GW150914.txt')
max_scale=1024
mother_freq=0.3
ylims=(0,512)
xlims=(-0.15,0.015)

times=strain[:,0]
strain=strain[:,1]


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Wavelet analysis
#
cwt_result = build_cwt(strain, times, max_scale=max_scale,
        mother_freq=mother_freq)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Plot wavelet-map
#

pl.close()
fig, ax_cont = plot_map(cwt_result, xlims, ylims)
pl.show()

