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
import json


class Stylelint_d(NodeLinter):
    """Provides an interface to stylelint_d."""

    syntax = ('css', 'sass', 'scss', 'postcss', 'less')
    cmd = ('stylelint_d', '--stdin', '--formatter=json', '--file', '@')
    npm_name = 'stylelint_d'
    version_args = '--version'
    version_re = r'(?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 1.0.8'
    line_col_base = (1, 1)
    error_stream = util.STREAM_BOTH
    comment_re = r'\s*/[/*]'
    selectors = {
        'html': 'source.css.embedded.html'
    }

    # https://github.com/kungfusheep/SublimeLinter-contrib-stylelint/blob/master/linter.py
    # Adapted from SublimeLinter-contrib-stylelint
    regex = (
        r'^\s*(?P<line>[0-9]+)\:(?P<col>[0-9]+)\s*'
        r'(?:(?P<error>error)|(?P<warning>warning))\s*'
        r'(?P<message>.+)'
    )

    # https://github.com/SublimeLinter/SublimeLinter-csslint/blob/master/linter.py
    # Taken from SublimeLinter-csslint
    word_re = r'^(#?[-\w]+)'

    def run(self, cmd, code):
        """Parse returned JSON into SublimeLinter friendly text."""

        raw = super().run(cmd, code)
        try:
            parsed = json.loads(raw)
            result = []

            for error in parsed[0]['warnings']:
                result.append("{}:{} {} {}".format(
                    error['line'],
                    error['column'],
                    error['severity'],
                    error['text'])
                )

            return "\n".join(result)
        except ValueError:
            return raw
