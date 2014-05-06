#!/usr/bin/env python3

import os

def read_func(f):
	lst = []
	with open(f, 'r') as read:
		ls = read.readlines()
		for a in ls:
			lst.append(a)
	return lst
