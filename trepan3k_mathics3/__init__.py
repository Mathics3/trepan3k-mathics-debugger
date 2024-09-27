# -*- coding: utf-8 -*-
#  Copyright (C) 2024 Rocky Bernstein <rocky@gnu.org>
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
trepan3k plugin which adds command `mathics3`.
This adds Mathics3 debugging support from inside trepan3k.

Authors: Rocky Bernstein rb@dustyfeet.com

License: GPL3

"""
__docformat__ = "restructuredtext"
from trepan3k_mathics3 import mathics3, mbacktrace, mup, printelement
from trepan3k_mathics3.version import __version__

__all__ = ["__version__", "mathics3", "mbacktrace", "mup", "printelement"]
