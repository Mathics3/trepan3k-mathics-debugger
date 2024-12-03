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
from pymathics.trepan.processor.command.backtrace import BacktraceCommand

BacktraceCommand.aliases = ("mbt",)
BacktraceCommand.__doc__ = """**mbacktrace** [*options*] [*count*]

    Print backtrace of all stack frames, or innermost *count* frames.

    An arrow indicates the 'current frame'. The current frame determines
    the context used for many debugger commands such as expression
    evaluation or source-line listing.

    *options* are:

       -h | --help    - give this help
       -b | --builtin - show Mathics3 builtin methods
       -e | --expr    - show Mathics3 Expressions

    Examples:
    ---------

       mbacktrace      # Print a full stack trace
       mbacktrace 2    # Print only the top two entries

    """


# def setup(debugger, instance):
#     """
#     Setup we need to do in order to make the Mathics3 Debugger code in ``instance`` work in the
#     trepan3k debugger object ``debugger``
#     """
#     print(f"Mathics setup called with {debugger}:\n\tinstance {instance}")
#     # Make sure
#     instance.debugger.intf = debugger.intf

# Demo it
if __name__ == "__main__":
    from trepan.processor.command import mock as Mmock

    dbgr, cmd = Mmock.dbg_setup()
    command = BacktraceCommand(cmd)
    for cmdline in [
        "mbacktrace",
    ]:
        args = cmdline.split()
        cmd_argstr = cmdline[len(args[0]) :].lstrip()
        cmd.cmd_argstr = cmd_argstr
        command.run(args)
        pass
    pass
