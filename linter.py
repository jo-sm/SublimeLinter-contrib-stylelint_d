#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Joshua Smock
# Copyright (c) 2016 Joshua Smock
#
# License: MIT
#

"""This module exports the Stylelint_d plugin class."""

from SublimeLinter.lint import NodeLinter, util


class Stylelint_d(NodeLinter):
    """Provides an interface to stylelint_d."""

    syntax = ('css', 'sass', 'scss', 'postcss', 'less')
    cmd = ('stylelint_d', '@')
    executable = 'stylelint_d'
    version_args = '--version'
    version_re = r'(?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 1.0.4'
    line_col_base = (1, 1)
    error_stream = util.STREAM_BOTH
    comment_re = r'\s*/[/*]'
    selectors = {
        'html': 'source.css.embedded.html'
    }

    # https://github.com/kungfusheep/SublimeLinter-contrib-stylelint/blob/master/linter.py
    # Taken from SublimeLinter-contrib-stylelint
    regex = (
        r'^\s*(?P<line>[0-9]+)\:(?P<col>[0-9]+)\s*(?:(?P<error>)|(?P<warning>))\s*(?P<message>.+)'
    )

    # https://github.com/SublimeLinter/SublimeLinter-csslint/blob/master/linter.py
    # Taken from SublimeLinter-csslint
    word_re = r'^(#?[-\w]+)'
