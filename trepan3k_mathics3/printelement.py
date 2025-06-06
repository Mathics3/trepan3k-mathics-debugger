# -*- coding: utf-8 -*-
# Copyright (C) 2024-2025 Rocky Bernstein <rocky@gnu.org>
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
from pymathics.trepan.processor.command.printelement import PrintElementCommand

# Demo it
if __name__ == "__main__":
    from trepan.processor.command import mock as Mmock

    dbgr, cmd = Mmock.dbg_setup()
    command = PrintElementCommand(cmd)
    for cmdline in [
        "printelement",
    ]:
        args = cmdline.split()
        cmd_argstr = cmdline[len(args[0]) :].lstrip()
        cmd.cmd_argstr = cmd_argstr
        command.run(args)
        pass
    pass
