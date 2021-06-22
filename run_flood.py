# Plutus Bitcoin Brute Forcer
# Made by Isaac Delly
# https://github.com/Isaacdelly/Plutus

import os
import multiprocessing

import plutus
import newKeyGen
import hashIterator

def main(database):

	print('Working...')
	
	baseHash = os.urandom(32)
	incrementing = bytearray(baseHash)
	decrementing = bytearray(baseHash)

	while True:

		inc_key = newKeyGen.keygen(incrementing.hex())
		plutus.process(inc_key[0], inc_key[2], inc_key[3], database)
		plutus.process(inc_key[0], inc_key[2], inc_key[4], database)

		dec_key = newKeyGen.keygen(decrementing.hex())
		plutus.process(dec_key[0], dec_key[2], dec_key[3], database)
		plutus.process(dec_key[0], dec_key[2], dec_key[4], database)

		hashIterator.changeHash(incrementing, 1)
		hashIterator.changeHash(decrementing, -1)

		# hashIterator.decimal_print(incrementing)
		# hashIterator.decimal_print(decrementing)

if __name__ == '__main__':
	database = plutus.read_database()

	# for cpu in range(multiprocessing.cpu_count()):
	# for cpu in range(1):
		# multiprocessing.Process(target=main, args=(database, )).start()
	main(database)