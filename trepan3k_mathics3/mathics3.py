# -*- coding: utf-8 -*-
# Copyright (C) 2024 Rocky Bernstein <rocky@gnu.org>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Our local modules
from pymathics.debugger.processor.command.mathics3 import Mathics3Command

Mathics3Command.__doc__ = """**mathics3**

    Go into a Mathics3 session

    This command is usually used by Mathics3 developers for debugging.

    Example:
    --------

        mathics3
"""

def setup(debugger, instance):
    """
    Setup we need to do in order to make the Mathics3 Debugger code in ``instance`` work in the
    trepan3k debugger object ``debugger``
    """
    # Make sure
    instance.debugger.intf = debugger.intf

# Demo it
if __name__ == "__main__":
    from trepan.processor.command import mock as Mmock

    dbgr, cmd = Mmock.dbg_setup()
    command = Mathics3Command(cmd)
    for cmdline in [
        "mathics3",
    ]:
        args = cmdline.split()
        cmd_argstr = cmdline[len(args[0]) :].lstrip()
        cmd.cmd_argstr = cmd_argstr
        command.run(args)
        pass
    pass
