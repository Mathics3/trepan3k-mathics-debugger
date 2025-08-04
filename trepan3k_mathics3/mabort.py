# -*- coding: utf-8 -*-
# Copyright (C) 2025 Rocky Bernstein <rocky@gnu.org>
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
import ctypes
import threading

import trepan.processor.cmdproc as trepan_cmdproc
from mathics.core.interrupt import AbortInterrupt
from trepan.processor.command.base_cmd import DebuggerCommand

class AbortCommand(DebuggerCommand):
    """**abort**

    Abort the computation being interrupted set the final computation to $Aborted.

    Similar to Mathics3 command Abort[]


    See also:
    ---------

    See `continue` `exit` or `kill` for more forceful termination commands.

    `run` and `restart` restart the debugged program."""

    aliases = ("a", "abort")
    category = "support"
    max_args = 0
    short_help = "Abort computation"

    DebuggerCommand.setup(locals(), category="support", max_args=0)

    def nothread_quit(self, arg):
        """abort command when there's just one thread."""

        self.debugger.core.stop()
        self.debugger.core.execution_status = "Abort command"
        raise AbortInterrupt

    def threaded_quit(self, arg):
        """abort command when several threads are involved."""
        threading_list = threading.enumerate()
        mythread = threading.current_thread()
        for t in threading_list:
            if t != mythread:
                ctype_async_raise(t, AbortInterrupt)
                pass
            pass
        raise AbortInterrupt

    def run(self, args):
        threading_list = threading.enumerate()
        if (
            len(threading_list) == 1 or self.debugger.from_ipython
        ) and threading_list[0].name == "MainThread":
            # We are in a main thread and either there is one thread or
            # we or are in ipython, so that's safe to quit.
            return self.nothread_quit(args)
        else:
            return self.threaded_quit(args)
        return



trepan_cmdproc.PASSTHROUGH_EXCEPTIONS.add(AbortInterrupt)
def setup(debugger, instance):
    """
    Setup we need to do in order to make the Mathics3 Debugger code in ``instance`` work in the
    trepan3k debugger object ``debugger``
    """
    # Make sure we hook into debugger interface
    print("mabort setup")
    instance.debugger.intf = debugger.intf
    trepan_cmdproc.PASSTHROUGH_EXCEPTIONS.add(AbortInterrupt)

# Demo it
if __name__ == "__main__":
    from trepan.processor.command import mock as Mmock

    dbgr, cmd = Mmock.dbg_setup()
    command = AbortCommand(cmd)
    for cmdline in [
        "abort",
    ]:
        args = cmdline.split()
        cmd_argstr = cmdline[len(args[0]) :].lstrip()
        cmd.cmd_argstr = cmd_argstr
        command.run(args)
        pass
    pass
