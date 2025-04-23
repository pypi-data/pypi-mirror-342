#!/usr/bin/env python

'''README

Usage:
  ./powerjira.py init
  ./powerjira.py goto
  ./powerjira.py fetch <target>
  ./powerjira.py make
  ./powerjira.py watched list
  ./powerjira.py watched prune
'''

from powerjira_toolchain.commands import app

if __name__ == "__main__":
  app()
