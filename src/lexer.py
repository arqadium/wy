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

import re

SYNTAX = {
    'def': {},
    'expr': {},
    'spec': {}
}

SYNTAX['order'] = [
    'eof',
    'eol',
    'space',
    'bcom',
    'lcom',
    'string',
    'char',
    'rident',
    'ident',
    'numdec',
    'numoct',
    'numhex',
    'numbin',
    'symbol'
]

SYNTAX['def']['eof'] = u'\u0000|\u001A'
SYNTAX['def']['eol'] = u'\u000A|\u000D|\u000D\u000A|\u2028|\u2029|' + \
    SYNTAX['def']['eof']
SYNTAX['def']['space'] = u'\u0009|\u000B|\u000C|\u0020'
SYNTAX['def']['lcom'] = '//((?!' + SYNTAX['def']['eol'] + ').)*(?=(' + \
    SYNTAX['def']['eol'] + '))'
SYNTAX['def']['bcom'] = r'/\*(.*)\*/'
SYNTAX['def']['string'] = r'"([^"]|\\")*"'
SYNTAX['def']['char'] = r"'([^']|\\\\')*'" # Not actually a char, OK
SYNTAX['def']['ident'] = r'\b[A-Za-z_][A-Za-z0-9_]*\b'
SYNTAX['def']['rident'] = r'\$\{[^\$\}\.:]+([\.:]([^\$\}\.:]+))*\}'
SYNTAX['def']['numdec'] = r'\b[0-9]+(\.[0-9]+)?\b'
SYNTAX['def']['numoct'] = r'\b0o[0-7]+\b'
SYNTAX['def']['numhex'] = r'\b0x[0-9A-Fa-f]+\b'
SYNTAX['def']['numbin'] = r'\b0b[0-1]+\b'
SYNTAX['def']['symbol'] = r'[\{\}~\$\[\],;:\.=]'
#SYNTAX['def'][''] = 

REFLAGS = re.UNICODE | re.MULTILINE

for key in SYNTAX['def']:
    SYNTAX['expr'][key] = re.compile(SYNTAX['def'][key], REFLAGS)

SYNTAX['spec']['nbcom'] = {
    'start': re.compile(r'/\+'),
    'end': re.compile(r'\+/', REFLAGS)
}

def lex(inText):
    inTextLen = len(inText)
    orderLR = range(len(SYNTAX['order']))
    inTextDup = inText[:]
    outTokens = []
    nestLevel = 0
    while len(inTextDup) > 0:
        advLen = 1 # Next character if no match is found
        if nestLevel > 0:
            match = SYNTAX['spec']['nbcom']['end'].match(inTextDup)
            if match != None:
                advLen = len(match.group(0))
                nestLevel -= 1
            continue
        # Not looping over the values themselves,
        # as they may be out-of-order
        for i in orderLR:
            key = SYNTAX['order'][i]
            # .match() only looks from the beginning
            match = SYNTAX['expr'][key].match(inTextDup)
            if match != None:
                # Ignore the rest of the match afterward
                advLen = len(match.group(0))
                outTokens += [{'type': key, 'match': match}]
                break
        match = SYNTAX['spec']['nbcom']['start'].match(inTextDup)
        if match != None:
            advLen = len(match.group(0))
            nestLevel += 1
            continue
        # Advance reading by a slice
        inTextDup = inTextDup[advLen:]
    return outTokens

def main(args):
    argc = len(args)
    if argc == 1:
        print('Good morning, Vietnam!')
        return 0
    from sys import stdout
    with open(args[1], 'r') as f:
        tokens = lex(f.read())
        tokensLR = range(len(tokens))
        for i in tokensLR:
            type = tokens[i]['type']
            match = tokens[i]['match']
            if type == 'space' or type == 'eol':
                continue
            print(type + ': ‘' + match.group(0) + '’')
    print('\nAll done.\n')
    return 0

if __name__ == '__main__':
    from sys import argv, exit
    exit(main(argv))
