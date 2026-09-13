# -*- coding: utf-8 -*-
#
#  Copyright (C) 2026 Rocky Bernstein
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
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import inspect
import sys
from typing import Optional

from mathics.core.evaluation import Evaluation
from mathics.core.rules import FunctionApplyRule
from trepan.processor.cmdbreak import set_break

# Our local modules
from trepan.processor.command.base_cmd import DebuggerCommand

from trepan3k_mathics3.parse.parser import LocationError
from trepan3k_mathics3.parse.scanner import ScannerError
from trepan3k_mathics3.parse.semantics import Location, build_bp_expr

# from trepan.processor.complete_rl import complete_break_linenumber


def find_evaluation(frame) -> Optional[Evaluation]:
    evaluation = None
    frame = frame.f_back
    while frame is not None:
        if (
            hasattr(frame, "f_locals")
            and (evaluation := frame.f_locals.get("evaluation", None))
            and isinstance(evaluation, Evaluation)
        ):
            return evaluation
        frame = frame.f_back
    return None


def parse_break_cmd(proc, text: str) -> Optional[list[Location]]:
    try:
        bp_expr = build_bp_expr(text)
    except LocationError as e:
        proc.errmsg("Error in parsing breakpoint expression at or around:")
        proc.errmsg(e.text)
        proc.errmsg(e.text_cursor)
        return None
    except ScannerError as e:
        proc.errmsg("Lexical error in parsing breakpoint expression at or around:")
        proc.errmsg(e.text)
        proc.errmsg(e.text_cursor)
        return None

    location = bp_expr.location
    condition = bp_expr.condition

    if location.method is None:
        proc.errmsg("Lexical error finding a Mathics3 builtin function name")
        return None

    try:
        return resolve_locations(sys._getframe(), proc, location.method)
    except ValueError as e:
        proc.errmsg(str(e))
        return None


def resolve_locations(start_frame, proc, builtin_fn_name: str) -> list[Location]:
    """Get trepan3k breakpointable locations given Mathics3 builtin function builtin_fn_name.
    start_frame is used to find an evaluation object that we can look up the rule definitions
    for builtin_fn_name.
    """
    if (
        not isinstance(evaluation := find_evaluation(start_frame), Evaluation)
        or evaluation is None
    ):
        proc.errmsg(
            "Cannot find an evaluation object in call stack to resolve {location.method}"
        )
        return []

    downvalue_rules = evaluation.definitions.get_downvalues(builtin_fn_name)
    if downvalue_rules is None:
        return []
    locations = []
    for rule in downvalue_rules:
        if isinstance(rule, FunctionApplyRule) and inspect.ismethod(
            bound_method := rule.rhs
        ):
            eval_func = bound_method.__func__
            locations.append(
                Location(
                    inspect.getsourcefile(eval_func),
                    eval_func.__code__.co_firstlineno,
                    False,
                    eval_func,
                    0,
                )
            )
    return locations


# import sys
# from trepan.api import run_call
# try:
#     ret = sys.call_tracing(run_call, (resolve_location, )
# except Exception as e:
#     print(f"Exception {e}")
# else:
#     print("R=> %s" % ret)


class MBreakCommand(DebuggerCommand):
    """**mbreak** [*location*] [if *condition*]]

    Sets a breakpoint, i.e. stopping point on a Builtin-function.

    If the word `if` is given after *location*, subsequent arguments given
    Without arguments or an empty *location*, the breakpoint is set
    the current stopped location.

    Normally we only allow stopping at lines that we think are
    stoppable. If the command has a `!` suffix, force the breakpoint anyway.

    Examples:
    ---------

       mbreak Refine        # Break on the Refine[] Mathics3 builtin function
       mbreak Plus          # Break pon the Plus[] or + Mathics3 builtin

    See also:
    ---------

    `break` `info break`, `tbreak`, `condition` and `help syntax location`."""

    aliases = ("mbrk", "mbreak!", "mb!")
    short_help = "Set breakpoint at a Mathics3 builtin command"

    DebuggerCommand.setup(locals(), category="breakpoints", need_stack=True)

    # complete = complete_break_linenumber

    def run(self, args):
        force = True if args[0][-1] == "!" else False

        locations = parse_break_cmd(self.proc, args[1])
        if locations:
            for location in locations:
                set_break(
                    self,
                    location.method,
                    location.path,
                    location.line_number,
                    None,
                    False,
                    args,
                    force=force,
                    offset=location.offset,
                )
        else:
            self.errmsg(f"Do not recognize find builtin function: {args[1]}")
        return


def setup(debugger, instance):
    """
    Setup we need to do in order to make the Mathics3 Debugger code in ``instance`` work in the
    trepan3k debugger object ``debugger``
    """
    # Make sure we hook into debugger interface.
    print("XXX3 setup called")
    instance.debugger.intf = debugger.intf


if __name__ == "__main__":
    from mathics.core.load_builtin import import_and_load_builtins
    from mathics.session import MathicsSession
    from trepan.processor.command import mock as Mmock

    import_and_load_builtins()
    session = MathicsSession(character_encoding="ASCII")
    # We need a local variable called evaluation of type Evaluation
    # set for the mbreak command to check for builtin functions.
    # so we set it here
    evaluation = session.evaluation

    dbgr, cmd = Mmock.dbg_setup()
    command = MBreakCommand(cmd)

    for cmdline in [
        "mbreak Refine",
    ]:
        args = cmdline.split()
        cmd_argstr = cmdline[len(args[0]) :].lstrip()
        cmd.cmd_argstr = cmd_argstr
        command.run(args)
        pass
    pass
