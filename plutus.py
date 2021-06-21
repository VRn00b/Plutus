import os
import pickle
import hashlib
import binascii

DATABASE = r'database/JUNE_9_2021/'

def read_database():
	"""
	Deserialize the database and read into a list of sets for easier selection 
	and O(1) complexity. Initialize the multiprocessing to target the main 
	function with cpu_count() concurrent processes.
	"""
	database = [set() for _ in range(4)]
	count = len(os.listdir(DATABASE))
	half = count // 2
	quarter = half // 2
	for c, p in enumerate(os.listdir(DATABASE)):
		print('\rreading database: ' + str(c + 1) + '/' + str(count), end=' ')
		with open(DATABASE + p, 'rb') as file:
			if c < half:
				if c < quarter:
					database[0] = database[0] | set(pickle.load(file))
				else:
					database[1] = database[1] | set(pickle.load(file))
			else:
				if c < half + quarter:
					database[2] = database[2] | set(pickle.load(file))
				else:
					database[3] = database[3] | set(pickle.load(file))
	print('DONE')

	# To verify the database size, remove the # from the line below
	#print('database size: ' + str(sum(len(i) for i in database))); quit()

	return database

def private_key_to_WIF(private_key):
	"""
	Convert the hex private key into Wallet Import Format for easier wallet 
	importing. This function is only called if a wallet with a balance is 
	found. Because that event is rare, this function is not significant to the 
	main pipeline of the program and is not timed.
	"""
	digest = hashlib.sha256(binascii.unhexlify('80' + private_key)).hexdigest()
	var = hashlib.sha256(binascii.unhexlify(digest)).hexdigest()
	var = binascii.unhexlify('80' + private_key + var[0:8])
	alphabet = chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
	value = pad = 0
	result = ''
	for i, c in enumerate(var[::-1]):
		value += 256**i * c
	while value >= len(alphabet):
		div, mod = divmod(value, len(alphabet))
		result, value = chars[mod] + result, div
	result = chars[value] + result
	for c in var:
		if c == 0:
			pad += 1
		else:
			break
	return chars[0] * pad + result

def process(private_key, public_key, address, database, words = ""):
	"""
	Accept an address and query the database. If the address is found in the 
	database, then it is assumed to have a balance and the wallet data is 
	written to the hard drive. If the address is not in the database, then it 
	is assumed to be empty and printed to the user.
	Average Time: 0.0000026941 seconds
	"""
	if address in database[0] or \
	   address in database[1] or \
	   address in database[2] or \
	   address in database[3]:
		with open('plutus.txt', 'a') as file:
			file.write('hex private key: ' + str(private_key) + '\n' +
					   'WIF private key: ' + str(private_key_to_WIF(private_key)) + '\n' +
					   'public key: ' + str(public_key) + '\n' +
					   'words: ' + str(words) + '\n' +
					   'address: ' + str(address) + '\n\n')
			print('found!')
	#else:
	#    pass
	#    #print(str(address))