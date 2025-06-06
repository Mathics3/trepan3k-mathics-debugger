Trepan3k plugin to support Mathics3 debugging from trepan3k
===========================================================

Abstract
--------

Here, we have a module extension for the trepan3k debugger that adds
commands that largely filter out and interpret Python information into
a more Mathics3-centric information.

Install
-------

::

   $ pip install -e .


Example
-------

::

   $ mathics3 --post-mortem  # goes into trepan3k post-mortem debugger on error.
   In[1]:= (* Put something here that that triggers a bug in Mathics3 *)
   Traceback (most recent call last):
     File "/tmp/Mathics3/mathics-core/mathics/core/expression.py", line 1907, in _is_neutral_symbol
       definition = definitions.get_definition(symbol_name, only_if_exists=True)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
     File "/src/external-vcs/github/Mathics3/mathics-core/mathics/core/definitions.py", line 506, in get_definition
       raise KeyError
   KeyError
   (Trepan3k:pm) load trepan3k_mathics3
   loaded command: "mathics3"
   loaded command: "mbacktrace"
   loaded command: "mdown"
   loaded command: "mup"
   loaded command: "printelement"
   (Trepan3k:pm) (Trepan3k:pm) help mbacktrace
   mbacktrace [options] [count]

       Print backtrace of all stack frames, or innermost count frames.


       An arrow indicates the 'current frame'. The current frame determines
       the context used for many debugger commands such as expression
       evaluation or source-line listing.


       options are:


          -h | --help    - give this help
          -b | --builtin - show Mathics3 builtin methods
          -e | --expr    - show Mathics3 Expressions


       Examples:
       ---------


          mbacktrace      # Print a full stack trace
          mbacktrace 2    # Print only the top two entries





   Aliases: mbt.

   (Trepan3k:pm) mbacktrace -e
   E:0 (3) Expression.restructure <class 'mathics.core.expression.Expression'>
            restructure(reparseUnterminatedGroupNode[{args}, bytes, FilterRules[{Sequence[]}, Options[reparseUnterminatedGro...),
   	head=<Symbol: CodeParser`Private`reparseUnterminatedGroupNode>, elements=[<Expression: <SymbolConsta...)
        called from file '/tmp/Mathics3/mathics-core/mathics/core/expression.py' at line 1138
   E:1 (4) Expression._flatten_sequence <class 'mathics.core.expression.Expression'>
            _flatten_sequence(reparseUnterminatedGroupNode[{args}, bytes, FilterRules[{Sequence[]}, Options[reparseUnterminatedGro...),
   	sequence=<function Expression.flatten_pattern_sequence.<locals>.sequence at 0x77d671362ac0>, evaluat...)
        called from file '/tmp/Mathics3/mathics-core/mathics/core/expression.py' at line 418
   E:2 (5) Expression.flatten_pattern_sequence <class 'mathics.core.expression.Expression'>
            flatten_pattern_sequence(reparseUnterminatedGroupNode[{args}, bytes, FilterRules[{Sequence[]}, Options[reparseUnterminatedGro...),
   	evaluation=<mathics.core.evaluation.Evaluation object at 0x77d671c18f50>)
        called from file '/tmp/Mathics3/mathics-core/mathics/core/expression.py' at line 644
