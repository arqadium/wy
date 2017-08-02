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

def main(args):
    print('Good morning, Vietnam!')
    return 0

if __name__ == '__main__':
    from sys import argv, exit
    exit(main(argv))
