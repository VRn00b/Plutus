# Plutus Bitcoin Brute Forcer
# Made by Isaac Delly
# https://github.com/Isaacdelly/Plutus

import multiprocessing
import bitcoinlib

import plutus
import oldKeyGen
import newKeyGen

def main(database):
	
	print('Working...')
	
	while True:

		# Mnemonic
		# words = bitcoinlib.mnemonic.Mnemonic().generate()
		# key = bitcoinlib.keys.HDKey().from_passphrase(words)
		
		# private = str(key)
		# public = key.public()
		
		# plutus.process(private, public, key.address(), database, words)
		# plutus.process(private, public, key.address_uncompressed(), database, words)
		
		# Improved
		key = newKeyGen.keygen_random()
		plutus.process(key[0], key[2], key[3], database)
		plutus.process(key[0], key[2], key[4], database)

		# Original
		# private_key = oldKeyGen.generate_private_key()
		# public_key = oldKeyGen.private_key_to_public_key(private_key)
		# address = oldKeyGen.public_key_to_address(public_key)
		# plutus.process(private_key, public_key, address, database)

if __name__ == '__main__':
	database = plutus.read_database()

	# for cpu in range(multiprocessing.cpu_count()):
	# for cpu in range(1):
		# multiprocessing.Process(target=main, args=(database, )).start()
	main(database)
