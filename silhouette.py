#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import os

class State:
    awaitNonspace = 1
    awaitNewline = 2

SOLID = '█'

def silhouette(infile, solid=None, start_solid=None, end_solid=None):
    '''Silhouete implements a basic state machine which produces the
    'silhouette' of files provided as input. A string like the following:
        a
          b
            c
              d
            cc
          bb
        aa
    Results in output like this:
        █
          █
            █
              █
            ██
          ██
        ██
        '''
    if solid == None:
        solid = SOLID
    if start_solid == None:
        start_solid = ''
    if end_solid == None:
        end_solid = ''
    state = State.awaitNonspace
    while True:
        c = infile.read(1)
        if not c:
            break
        if state == State.awaitNonspace:
            if not c.isspace():
                state = State.awaitNewline
                yield start_solid+solid
            else:
                yield c.replace("\t", "    ")
        elif state == State.awaitNewline:
            if c == '\n':
                state = State.awaitNonspace
                yield end_solid+c
            else:
                yield solid

def main():
    if not os.isatty(sys.stdin.fileno()):
        for c in silhouette(sys.stdin):
            print(c, end="")
    elif len(sys.argv) > 1:
        for path in sys.argv[1:]:
            with open(path) as f:
                for c in silhouette(f):
                    print(c, end="")
    else:
        usage = '''{name}: missing file input

Usage: {name} [files]

Prints the "silhouette" of files listed in args or data from stdin.'''
        print(usage.format(name=sys.argv[0]))

if __name__ == '__main__':
    main()
