#!/usr/bin/env python3


def write_func(lst, f, name, value):
	i = 0
	while i < len(lst):
		if name == lst[i][0:lst[i].find("=")]:
			if name == "Theme":
				lst[i] = name + "=" + str(value) + "\n"
			else:
				lst[i] = name + "=" + str(value).lower() + "\n"
		i += 1		
	with open(f, 'w') as wr:
		for b in lst:
			wr.write(b)
