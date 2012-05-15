#!/usr/bin/python

import random

if __name__ == '__main__': 
    random.seed()
    for i in xrange(20):
    	print random.randint(-127,128)
