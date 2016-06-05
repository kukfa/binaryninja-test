#!/usr/bin/python

import sys, time
sys.path.insert(0, 'binaryninja/python')
import binaryninja

bv = binaryninja.BinaryViewType["ELF"].open("bomb")
bv.update_analysis()
time.sleep(0.1)

# find phase_1
for fn in bv.functions:
	if fn.symbol.name == "phase_1":
		phase_1 = fn

# loop through instructions in phase_1's main block
for instr in phase_1.low_level_il.basic_blocks[0]:
	# get address of string comparison function
	if instr.operation == binaryninja.core.LLIL_CALL:
		callAddr = instr.address

# get address of comparison string
strAddr = phase_1.get_parameter_at(bv.arch, callAddr, None, 1).value

# get the length of comparison string
strLen = 0
curr = bv.read(strAddr, 1).encode('hex')
while (curr != "2e") and (curr != "00"):
	strLen += 1
	curr = bv.read(strAddr + strLen, 1).encode('hex')

# get the comparison string
cmpStr = bv.read(strAddr, strLen)
print cmpStr
