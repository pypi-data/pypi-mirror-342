# -*- coding: utf-8 -*-
# examples\scene_signals.py

"""
    Module for the creation of three typical excitation signal files.

    Creates the needed excitation signal `.wav` files for the Audio Simulation
    Module, of the Horizon project SCENE. The produced signals have durations
    of 743 ms, 2972 ms, and 11889 ms, corresponding to typical small, medium
    and large rooms. All the files are stored in the `output` subdirectory, in
    the execution path.

    Copyright (C) 2025 Christos Sevastiadis

    Usage:
    ```>python.exe scene_signals.py```

    or
    ```>python3 scene_signals.py```

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

from scene_rir import rir

# Swept-sine excitation signals creation

# Short duration time signal, for small rooms
ss_params_1 = {
    "sglszeidx": 1,
}
ss_signal_1 = rir.SweptSineSignal(ss_params_1)
ss_signal_1.save("output/ss-signal-44100_kHz-743_ms.wav")

# Medium duration time signal, for medium rooms
ss_params_2 = {
    "sglszeidx": 3,
}
ss_signal_2 = rir.SweptSineSignal(ss_params_2)
ss_signal_2.save("output/ss-signal-44100_kHz-2972_ms.wav")

# Long duration time signal, for large rooms
ss_params_3 = {
    "sglszeidx": 5,
}
ss_signal_3 = rir.SweptSineSignal(ss_params_3)
ss_signal_3.save("output/ss-signal-44100_kHz-11889_ms.wav")
