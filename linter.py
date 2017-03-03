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
    version_re = r'(?P<version>\d+\.\d+\.[0-9]?[0-9a-z]+)'
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
        r'^\s*(?P<line>[0-9]*)\:(?P<col>[0-9]*)\s*'
        r'(?:(?P<error>error)|(?P<warning>warning)|(?P<deprecation>deprecation)|(?P<invalid>invalid))\s*'
        r'(?P<message>.+)'
    )

    # https://github.com/SublimeLinter/SublimeLinter-csslint/blob/master/linter.py
    # Taken from SublimeLinter-csslint
    word_re = r'^(#?[-\w]+)'

    def split_match(self, match):
        """Override `split_match` to support invalidOptionWarnings and deprecations."""

        if match:
            group = match.groupdict()
            if group.get('deprecation') or group.get('invalid'):
                # We have to show the error on some line or else it won't
                # show in Sublime
                return match, 0, 0, True, False, group.get('message'), None
            else:
                return super().split_match(match)
        else:
            return super().split_match(match)

    def run(self, cmd, code):
        """Parse returned JSON into SublimeLinter friendly text."""

        raw = super().run(cmd, code)

        try:
            parsed = json.loads(raw)
        except ValueError:
            return []

        result = []

        try:
            file_errors = parsed[0]  # Parsed is an array of each file data
        except IndexError:
            return []

        for error in file_errors.get('deprecations', []):
            result.append("0:0 deprecation {}".format(error.get('text')))

        for error in file_errors.get('invalidOptionWarnings', []):
            result.append('0:0 invalid {}'.format(error.get('text')))

        for error in file_errors.get('warnings', []):
            # Severity may not be present in the warning
            result.append("{}:{} {} {}".format(
                error.get('line', '0'),
                error.get('column', '0'),
                error.get('severity', 'error'),
                error.get('text', ''))
            )

        return "\n".join(result)
