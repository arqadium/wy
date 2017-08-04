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

import lex, yacc

tokens = [
    'EOF',
    'EOL',
    'SPACE',
    'LCOM',
    'BCOM',
    'NBCOM',
    'STRING',
    'QUOTE1',
    'QUOTE2',
    'IDENT',
    'REF',
    'NUMERIC',
    'BRACE_L',
    'BRACE_R',
    'ASSIGN',
    'COMMA',
    'TILDE',
    'BRACKET_L',
    'BRACKET_R'
]

t_EOF = u'\u0000|\u001A'
t_ignore = u'\u0009|\u000B|\u000C|\u0020'
t_IDENT = r'\b[A-Za-z_][A-Za-z0-9_]*\b'
t_NUMERIC = 
t_BRACE_L = r'\{'
t_BRACE_R = r'\}'
t_ASSIGN = r'\='
t_COMMA = r'\,'
t_TILDE = '~'
t_BRACKET_L = r'\['
t_BRACKET_R = r'\]'

def t_EOL(t):
    u';|\\r\\n|\\r|\\n|\u2028|\u2029|\u0000|\u001A'
    t.lexer.lineno += len(t.value)
    return t

def t_NUMERIC(t):
    r'\b([0-9]+(\.[0-9]+)?|0o[0-7]+|0x[0-9A-Fa-f]+|0b[0-1]+|[\+\-]?Infinity|NaN)\b'
    if t.value == '-Infinity':
        t.value = float('-inf')
    elif t.value.endswith('Infinity'):
        t.value = float('+inf')
    elif t.value == 'NaN':
        t.value = float('nan')
    else:
        t.value = int(t.value)
    return t

def t_SPACE(t):
    r'\s+'
    t.lexer.lineno += t.value.count("\n")
    return t

def t_NBCOM(t):
    r'/\+(.|\n)*?\+/'
    ncr = t.value.count("\n")
    t.lexer.lineno += ncr
    # replace with one space or a number of '\n'
    t.type = 'SPACE'; t.value = '\n' * ncr if ncr else ' '
    return t

# Comment
def t_BCOM(t):
    r'(/\*(.|\n)*?\*/)'
    ncr = t.value.count("\n")
    t.lexer.lineno += ncr
    # replace with one space or a number of '\n'
    t.type = 'SPACE'; t.value = '\n' * ncr if ncr else ' '
    return t

# Line comment
def t_LCOM(t):
    r'(//.*?(\n|$))'
    # replace with '\n'
    t.type = 'SPACE'; t.value = '\n'
    return t

def t_QUOTE1(t):
    r"'([^\\\n]|(\\(.|\n)))*?'"
    t.type = 'STRING'
    t.value = t.value[1:-1]
    t.lexer.lineno += t.value.count('\n')
    return t

def t_QUOTE2(t):
    r'"([^\\\n]|(\\(.|\n)))*?"'
    t.type = 'STRING'
    t.value = t.value[1:-1]
    t.lexer.lineno += t.value.count('\n')
    return t

def t_REF(t):
    r'\$\{([^\}\r\n]+)\}'
    t.lexer.lineno += t.value.count('\n')
    return t

def t_error(t):
    print('Illegal character: ' + t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

start = 'stmt'

class Node:
    def __init__(self, type, children=None, leaf=None):
         self.type = type
         if children:
              self.children = children
         else:
              self.children = []
         self.leaf = leaf
    def __getitem__(self, key):
        return self.children[key]

def p_ident(p):
    '''ident : IDENT 
             | STRING'''
    pass

def p_expr_ref(p):
    '''ref : REF
           | REF TILDE ref'''
    if len(p) < 4:
        p[0] = Node('ref', [p[1]])
    else:
        p[0] = Node('ref', [p[1]] + p[3])

def p_expr_num(p):
    'num : NUMERIC'
    p[0] = Node('num', [p[1]])

def p_expr_str(p):
    '''str : STRING
           | STRING TILDE REF
           | REF TILDE STRING
           | STRING TILDE str
           | str TILDE STRING'''
    if len(p) < 4:
        p[0] = Node('str', [p[1]])
    elif p[3].startswith('$'):
        p[0] = Node('str_ref', [p[1], p[3]])
    elif p[1].startswith('$'):
        p[0] = Node('str_ref', [p[3], p[1]])
    elif type(p[1]) != Node:
        p[0] = Node('str', [p[1]] + p[3])
    else:
        p[0] = Node('str', p[1] + [p[3]])

def p_expr_num_array(p):
    '''num_array : num
                 | num_array COMMA num
       str_array : str
                 | str_array COMMA str'''
    if len(p) < 4:
        p[0] = Node('array', [p[1]])
    else:
        p[0] = Node('array', p[1] + [p[3]])

def p_stmt(p):
    '''stmt : ident ASSIGN expr
            | ident BRACKET_L list BRACKET_R
            | ident BRACE_L stmt BRACE_R'''
    p[0] = ('statement', p[2], )

def main(args):
    argc = len(args)
    if argc == 1:
        print('Good morning, Vietnam!')
        return 0
    with open(args[1], 'rb') as f:
        lexer.input(f.read().decode('utf8', 'ignore'))
        for tok in lexer:
            print(tok.type, tok.value, tok.lineno, tok.lexpos)
    print('\nAll done.\n')
    return 0

if __name__ == '__main__':
    from sys import argv, exit
    exit(main(argv))
