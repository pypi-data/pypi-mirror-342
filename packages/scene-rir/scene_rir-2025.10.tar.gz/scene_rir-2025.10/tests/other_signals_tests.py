# -*- coding: utf-8 -*-
# tests\other_signals_tests.py

"""
    Module for the testing of the `scene_rir` package, over the other signals.

    This module tests the `scene_rir.rir` module. It uses an excitation signal
    generated from another source, and extracts the room impulse responses from
    three recorded responses in real rooms. The output results are plotted in
    diagrams.

    Copyright (C) 2025 Christos Sevastiadis

    Usage:
    ```>python.exe other_signals_tests.py```

    or
    ```>python3 other_signals_tests.py```

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

import rir_plot
from scene_rir import rir

#######################################################################

params = {
    "frqstp": 22000,
    "frqstt": 10,
    "rec_path": "input/GrCLab1SSRPos2.wav",
    "ref_path": "input/Sweep(10-22000Hz,10s-0.2s).wav",
}
irs_signal = rir.ImpulseResponseSignal(params)
irs_signal.save("output/irs-signal-GrCLab1SSRPos2.wav")

rir_plot.plot_irs(irs_signal)
rir_plot.plot_irs_deconvolution(irs_signal)

#######################################################################

params = {
    "frqstp": 22000,
    "frqstt": 10,
    "rec_path": r"input\GrCLab2SSRPos1Src1.wav",
    "ref_path": r"input\Sweep(10-22000Hz,10s-0.2s).wav",
}
irs_signal = rir.ImpulseResponseSignal(params)
irs_signal.save("output/irs-signal-GrCLab2SSRPos1Src1.wav")

rir_plot.plot_irs(irs_signal)
rir_plot.plot_irs_deconvolution(irs_signal)

#######################################################################

params = {
    "frqstp": 22000,
    "frqstt": 10,
    "rec_path": r"input\GrCLab2SSRPos1Src2.wav",
    "ref_path": r"input\Sweep(10-22000Hz,10s-0.2s).wav",
}
irs_signal = rir.ImpulseResponseSignal(params)
irs_signal.save("output/irs-signal-GrCLab2SSRPos1Src2.wav")

rir_plot.plot_irs(irs_signal)
rir_plot.plot_irs_deconvolution(irs_signal)

#######################################################################
