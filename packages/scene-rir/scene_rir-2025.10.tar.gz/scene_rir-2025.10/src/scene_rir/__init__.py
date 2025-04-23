# -*- coding: utf-8 -*-
# src\scene_rir\__init__.py

"""
    Room Impulse Response extraction package.

    The purpose of this package is to extract the room impulse response (RIR) from the
    recorded response signal of a proper excitation signal. It is part of the Audio
    Simulation Module of the Horizon project SCENE.

    Modules:
    - rir: Provides the classes implementing swept-sine excitation signal creation and
        room impulse response extraction from a recorded response.

    Examples:
    Example of usage from command line (Windows OS):
    > python -m scene_rir.rir
    Usage: python -m scene_rir.rir [command] [parameter1] [parameter2]
    or
    python3 -m scene_rir.rir [command] [parameter1] [parameter2]
    Available commands:
    save   Save the default swept-sine signal.

    > python -m scene_rir.rir --help
    Usage: python -m scene_rir.rir [command] [parameter1] [parameter2]
    or
    python3 -m scene_rir.rir [command] [parameter1] [parameter2]
    Available commands:
    save   Save the default swept-sine signal.

    > python -m scene_rir.rir save my_folder/my_signal.wav

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

__all__ = ["rir"]
__author__ = "Christos Sevastiadis <csevast@ece.auth.gr>"

from . import rir

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version  # for Python<3.8

__version__ = version(__name__)
