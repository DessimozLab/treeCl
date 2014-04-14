#!/usr/bin/env python
from __future__ import print_function
import sys

__all__ = ['print_and_return']

def print_and_return(s, file=sys.stdout):
    print('\r\x1b[K{0}'.format(s), end='', file=file) #\x1b[K = Esc+[K = clear line
    file.flush()

if __name__ == '__main__':
    #TEST
    import time

    for i in range(1,11):
        print_and_return(i)
        time.sleep(0.3)
    print()

    for i in range(1,21):
        print_and_return('.'*(22-i-len(str(i)))+str(i))
        time.sleep(0.3)
    print()