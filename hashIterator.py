import os

def changeHash(bytearray, delta):
	iterateHash(bytearray, len(bytearray) - 1, delta)

def iterateHash(bytearray, index, delta):
	carry = 0
	newValue = bytearray[index] + delta

	if newValue > 255:
		carry = 1
		newValue %= 256
	elif newValue < 0:
		carry = -1
		newValue = 256 + newValue
		
	bytearray[index] = newValue

	if carry != 0 and index > 0:
		iterateHash(bytearray, index - 1, carry)
	
	return bytearray

def decimal_print(bytearray):
	for i in bytearray:
		print(i, end =" ")
	print()