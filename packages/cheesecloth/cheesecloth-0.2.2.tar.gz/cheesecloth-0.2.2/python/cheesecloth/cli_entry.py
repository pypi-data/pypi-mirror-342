#!/usr/bin/env python3
"""
Cheesecloth CLI Entry Point
=========================

This module serves as the entry point for the cheesecloth-analyze command-line tool,
providing a streamlined way to access Cheesecloth's text analysis capabilities
from the command line.

The module is intentionally minimal, delegating the actual implementation to
the cli.py module. This separation enables:

1. Clean installation of the entry point through setuptools
2. Clear separation between implementation and command invocation
3. Proper packaging for command-line tools

When Cheesecloth is installed, this module creates the 'cheesecloth-analyze'
command that can be run from any terminal.

For full documentation on available options and usage examples,
see the cli.py module or run:

```
cheesecloth-analyze --help
```
"""

from cheesecloth.cli import main

if __name__ == "__main__":
    main()
