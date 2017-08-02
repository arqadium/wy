#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; indent-tabs-mode: nil; indent-width: 4; -*-
#
## Copyright © 2017 Arqadium. All rights reserved.
##
## This document contains proprietary information of ARQADIUM and/or its
## licensed developers and are protected by national and international
## copyright laws. They may not be disclosed to third parties or copied or
## duplicated in any form, in whole or in part, without the prior written
## consent of Arqadium.
##

from lexer import lex

class Node:
    children = []
    def __init__(self, type, match):
        self.type = type
        self.text = match.group(0)
        self.parts = match.groups()

def parse(tokens):
    return 

def main(args):
    if len(args) == 1:
        print('Good morning, Vietnam!')
        return 0
    from sys import stdout
    with open(args[1], 'r') as f:
        tokens = lex(f.read())
        ast = parse(tokens)
        # Yet to implement printing of AST
    print('\nAll done.\n')
    return 0

if __name__ == '__main__':
    from sys import argv, exit
    exit(main(argv))
