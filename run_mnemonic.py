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
		words = bitcoinlib.mnemonic.Mnemonic().generate()
		key = bitcoinlib.keys.HDKey().from_passphrase(words)
		
		private = str(key)
		public = key.public()
		
		plutus.process(private, public, key.address(), database, words)
		plutus.process(private, public, key.address_uncompressed(), database, words)
		
if __name__ == '__main__':
	database = plutus.read_database()

	# for cpu in range(multiprocessing.cpu_count()):
	# for cpu in range(1):
		# multiprocessing.Process(target=main, args=(database, )).start()
	main(database)
