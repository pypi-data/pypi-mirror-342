# -*- coding: utf-8 -*-
# tests\scene_signals_tests.py

"""
    Module for the testing of the `scene_rir` package, over the SCENE signals.

    This module tests the `scene_rir.rir` module. It uses the three excitation
    signals used in the Audio Simulation Module of the Horizon Europa project
    SCENE, as both reference and recorder response signals, producing Kronecker
    Delta responses, not delayed in time. The output results are plotted in
    diagrams.

    Copyright (C) 2025 Christos Sevastiadis

    Usage:
    ```>python.exe scene_signals_tests.py```

    or
    ```>python3 scene_signals_tests.py```

    License:
    GNU GPL v3.0

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

"""

__author__ = "Christos Sevastiadis <csevast@ece.auth.gr>"

import shutil
from pathlib import Path

import rir_plot
from scene_rir import rir

#######################################################################

DELAY_DURATION = 0
SIGNAL_LEVEL = -3

ss_params_1 = {
    "sglszeidx": 1,
}
ss_signal_1 = rir.SweptSineSignal(ss_params_1)
ss_signal_1.save("output/ss-signal-44100_kHz-743_ms.wav")

p = Path("input")
if not p.exists():
    p.mkdir(parents=True)
shutil.copy(
    "output/ss-signal-44100_kHz-743_ms.wav", "input/ss-signal-44100_kHz-743_ms.wav"
)

irs_params_1 = {
    "rec_path": "input/ss-signal-44100_kHz-743_ms.wav",
    "ref_path": "input/ss-signal-44100_kHz-743_ms.wav",
}
irs_signal_1 = rir.ImpulseResponseSignal(irs_params_1)
irs_signal_1.save("output/irs-signal-44100_kHz-743_ms.wav")

rir_plot.plot_irs(irs_signal_1)
rir_plot.plot_irs_deconvolution(irs_signal_1)
rir_plot.plot_irs_impulse(irs_signal_1, DELAY_DURATION, SIGNAL_LEVEL)

#######################################################################

DELAY_DURATION = 0
SIGNAL_LEVEL = -3

ss_params_2 = {
    "sglszeidx": 3,
}
ss_signal_2 = rir.SweptSineSignal(ss_params_2)
ss_signal_2.save("output/ss-signal-44100_kHz-2972_ms.wav")
p = Path("input")
if not p.exists():
    p.mkdir(parents=True)
shutil.copy(
    "output/ss-signal-44100_kHz-2972_ms.wav", "input/ss-signal-44100_kHz-2972_ms.wav"
)

irs_params_2 = {
    "rec_path": "input/ss-signal-44100_kHz-2972_ms.wav",
    "ref_path": "input/ss-signal-44100_kHz-2972_ms.wav",
}
irs_signal_2 = rir.ImpulseResponseSignal(irs_params_2)
irs_signal_2.save("output/irs-signal-44100_kHz-2972_ms.wav")

rir_plot.plot_irs(irs_signal_2)
rir_plot.plot_irs_deconvolution(irs_signal_2)
rir_plot.plot_irs_impulse(irs_signal_2, DELAY_DURATION, SIGNAL_LEVEL)

#######################################################################

DELAY_DURATION = 0
SIGNAL_LEVEL = -3

ss_params_3 = {
    "sglszeidx": 5,
}
ss_signal_3 = rir.SweptSineSignal(ss_params_3)
ss_signal_3.save("output/ss-signal-44100_kHz-11889_ms.wav")
p = Path("input")
if not p.exists():
    p.mkdir(parents=True)
shutil.copy(
    "output/ss-signal-44100_kHz-11889_ms.wav", "input/ss-signal-44100_kHz-11889_ms.wav"
)

irs_params_3 = {
    "rec_path": "input/ss-signal-44100_kHz-11889_ms.wav",
    "ref_path": "input/ss-signal-44100_kHz-11889_ms.wav",
}
irs_signal_3 = rir.ImpulseResponseSignal(irs_params_3)
irs_signal_3.save("output/irs-signal-44100_kHz-11889_ms.wav")

rir_plot.plot_irs(irs_signal_3)
rir_plot.plot_irs_deconvolution(irs_signal_3)
rir_plot.plot_irs_impulse(irs_signal_3, DELAY_DURATION, SIGNAL_LEVEL)
