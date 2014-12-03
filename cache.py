#!/usr/bin/python
# import the necessary libraries to make this thing run
import sys
import math

# create the cache
# set it to be an empty list
cache = []

# iterate over sets and add sets to cache as needed
for x in range(int(sys.argv[1])):
	curset = []
	#iterate over lines and add dictionaries to current set
	for x2 in range(int(sys.argv[2])):
		curset.append({'v': False, 't': 0, 'i':0, 'd':False})
	cache.append(curset)

# find s
s = int(math.ceil(math.log(int(sys.argv[1]),2)))

# do some magic to make a binary number to find our set
# make a string of all 1s... then and against that number
# (e.g., S = 3 -> 111. This will be ANDed later)
stringToBeIntifiedLater = ''
for x in xrange(0,s):
	stringToBeIntifiedLater += '1'

#find b
b = int(math.ceil(math.log(int(sys.argv[3]),2)))

# create an instruction counter
ic = 0

# read in the first line of info
line = sys.stdin.readline().strip()

#loop through input
while (line != ''):
	#split input on the space
	inputlist = line.split(' ')
	# get the address
	addr = int(inputlist[1])
	# get the block of the address
	# by shifting right 'b' spaces
	daBlock = addr >> b
	# use the magic from above to get set number
	setnum = (daBlock & int(stringToBeIntifiedLater,2))
	# create and set our variables
	hit = False
	write = False
	linenum = None
	evictedblock = '-'

	for line in cache[setnum]:
		if (line['v'] and line['t'] == daBlock):
			hit = True
			linenum = cache[setnum].index(line)
			line['i'] = ic
			if (inputlist[0] == 'write'):
				line['d'] = True
			break
	
	# we missed
	if (not hit):
		for line in cache[setnum]:
			if (not line['v']):
				linenum = cache[setnum].index(line)
				line['v'] = True
				line['t'] = daBlock
				line['i'] = ic
				if (inputlist[0] == 'write'):
					line['d'] = True
				break

		if (linenum is None):
			lowestnum = cache[setnum][0]['i']
			linenum = 0			
			for line in cache[setnum]:
				if (line['i'] < lowestnum):
					lowestnum = line['i']
					linenum = cache[setnum].index(line)

			evictedline = cache[setnum][linenum]
			if (evictedline['d']):
				write = True

			evictedblock = str(evictedline['t'])
			evictedline['v'] = True
			evictedline['t'] = daBlock
			evictedline['i'] = ic
			if (inputlist[0] == 'write'):
				evictedline['d'] = True
			else:
				evictedline['d'] = False

	# print our output
	print '{0} {1} {2} {3} {4} {5} {6}'.format(int(hit),int(not hit),daBlock if not hit else '-',
		setnum if not hit else '-',linenum if not hit else '-',int(write),evictedblock if write else '-')
	
	#increment program counter
	ic += 1

	#read next line
	line = sys.stdin.readline()