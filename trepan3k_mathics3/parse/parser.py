#  Copyright (c) 2017-2018, 2025 Rocky Bernstein
"""
Parsing for a Mathics3 trepan debugger
"breakpoint' or "list" command arguments

This is a debugger location along with:
 - an optional condition parsing for breakpoints commands
 - a range or count for "list" commands
"""

import sys
from typing import Final

from spark_parser import GenericASTBuilder
from spark_parser.ast import AST

from trepan3k_mathics3.parse.scanner import LocationScanner, ScannerError

DEFAULT_DEBUG: Final = {
    "rules": False,
    "transition": False,
    "reduce": False,
    "errorstack": None,
    "dups": False,
    "local_print": False,
}


class LocationError(Exception):
    def __init__(self, text, text_cursor):
        self.text = text
        self.text_cursor = text_cursor

    def __str__(self):
        return self.text + "\n" + self.text_cursor


class LocationParser(GenericASTBuilder):
    """Location parsing as used in trepan2 and trepan3k
    for list, breakpoint
    Note: function parse() comes from GenericASTBuilder
    """

    def __init__(self, start_nt, text, debug=None):
        super(LocationParser, self).__init__(AST, start_nt, debug=DEFAULT_DEBUG)
        self.debug = debug
        self.text = text

    def error(self, tokens, index):
        token = tokens[index]
        if self.debug.get("local_print", False):
            print(self.text)
            print(" " * (token.offset + len(str(token.value))) + "^")
            print("Syntax error at or near token '%s'" % token.value)
            if "context" in self.debug and self.debug["context"]:
                super(LocationParser, self).error(tokens, index)
        raise LocationError(
            self.text, " " * (token.offset + len(str(token.value))) + "^"
        )

    def nonterminal(self, nt, args):
        has_len = hasattr(args, "__len__")

        # collect = ('tokens',)
        # if nt in collect and len(args) > 1:
        #     #
        #     #  Collect iterated thingies together.
        #     #
        #     rv = args[0]
        #     for arg in args[1:]:
        #         rv.append(arg)

        if (
            has_len
            and len(args) == 1
            and hasattr(args[0], "__len__")
            and len(args[0]) == 1
        ):
            # Remove singleton derivations
            rv = GenericASTBuilder.nonterminal(self, nt, args[0])
            del args[0]  # save memory
        else:
            rv = GenericASTBuilder.nonterminal(self, nt, args)
        return rv

    ##########################################################
    # Expression grammar rules. Grammar rule functions
    # start with the name p_ and are collected automatically
    ##########################################################

    def p_bp_location(self, args):
        """
        bp_start    ::= tokens
        """

    # location that is used in breakpoints, list commands, and disassembly
    def p_location(self, args):
        """
        opt_space   ::= SPACE?

        location_if ::= location
        location_if ::= location SPACE IF tokens

        # Note no space is allowed between FILENAME COLON, and NUMBER
        location    ::= FUNCNAME

        # For tokens we accept anything. Were really just
        # going to use the underlying string from the part
        # after "if".  So below we all of the possible tokens

        tokens      ::= token+
        token       ::= FUNCNAME
        token       ::= NUMBER
        token       ::= OFFSET
        token       ::= SPACE
        """


def parse_location(
    start_symbol, text, out=sys.stdout, show_tokens=False, parser_debug=DEFAULT_DEBUG
):
    assert isinstance(text, str)
    tokens = LocationScanner().tokenize(text)
    if show_tokens:
        for t in tokens:
            print(t)

    # For heavy grammar debugging
    # parser_debug = {'rules': True, 'transition': True, 'reduce': True,
    #                 'errorstack': True, 'dups': True}
    # parser_debug = {'rules': False, 'transition': False, 'reduce': True,
    #                 'errorstack': 'full', 'dups': False}

    parser = LocationParser(start_symbol, text, parser_debug)
    # parser.check_grammar(frozenset(('bp_start', 'range_start', 'arange_start')))
    return parser.parse(tokens)


def parse_bp_location(*args, **kwargs):
    return parse_location("bp_start", *args, **kwargs)


if __name__ == "__main__":

    def doit(fn, line):
        try:
            ast = fn(line, show_tokens=True)
            print(ast)
        except ScannerError as e:
            print("Scanner error")
            print(e.text)
            print(e.text_cursor)
        except LocationError as e:
            print("Parser error at or near")
            print(e.text)
            print(e.text_cursor)

    # FIXME: we should make sure all of the below is in a unit test.

    # lines = """
    # /tmp/foo.py:12
    # /tmp/foo.py line 12
    # 12
    # ../foo.py:5
    # gcd()
    # foo.py line 5 if x > 1
    # """.splitlines()
    # for line in lines:
    #     if not line.strip():
    #         continue
    #     print("=" * 30)
    #     print(line)
    #     print("+" * 30)
    #     doit(parse_bp_location, line)

    # bad_lines = """
    # /tmp/foo.py
    # '''/tmp/foo.py'''
    # /tmp/foo.py 12
    # gcd()
    # foo.py if x > 1
    # """.splitlines()
    # for line in bad_lines:
    #     if not line.strip():
    #         continue
    #     print("=" * 30)
    #     print(line)
    #     print("+" * 30)
    #     doit(parse_bp_location, line)

    # lines = """
    # 1
    # 2,
    # ,3
    # 4,10
    # """.splitlines()
    # for line in lines:
    #     if not line.strip():
    #         continue
    #     print("=" * 30)
    #     print(line)
    #     print("+" * 30)
    #     doit(parse_range, line)
    #     print(ast)

    lines = ("Refine[]",)
    for line in lines:
        line = line.strip()
        if not line:
            continue
        print("=" * 30)
        print(line)
        print("+" * 30)
        doit(parse_bp_location, line)
