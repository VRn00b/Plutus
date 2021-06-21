import os
import hashlib
import binascii
import codecs
import ecdsa

def base58(address_hex):
	alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
	b58_string = ''
	# Get the number of leading zeros and convert hex to decimal
	leading_zeros = len(address_hex) - len(address_hex.lstrip('0'))
	# Convert hex to decimal
	address_int = int(address_hex, 16)
	# Append digits to the start of string
	while address_int > 0:
		digit = address_int % 58
		digit_char = alphabet[digit]
		b58_string = digit_char + b58_string
		address_int //= 58
	# Add '1' for each 2 leading zeros
	ones = leading_zeros // 2
	for one in range(ones):
		b58_string = '1' + b58_string
	return b58_string


def keygen_random():
	return keygen(os.urandom(32).hex())

def keygen(private):
	
	## PUBLIC UNCOMP
	public = b'04'+codecs.encode(ecdsa.SigningKey.from_string(codecs.decode(private, 'hex'), curve=ecdsa.SECP256k1).verifying_key.to_string(), 'hex')        
	public_key_bytes = codecs.decode(public, 'hex')

	## PUBLIC UNCOMP ADDRESS
	sha256_bpk = hashlib.sha256(public_key_bytes)
	sha256_bpk_digest = sha256_bpk.digest()
	ripemd160_bpk = hashlib.new('ripemd160')
	ripemd160_bpk.update(sha256_bpk_digest)
	ripemd160_bpk_digest = ripemd160_bpk.digest()
	ripemd160_bpk_hex = codecs.encode(ripemd160_bpk_digest, 'hex')
	network_byte = b'00'
	network_bitcoin_public_key = network_byte + ripemd160_bpk_hex
	network_bitcoin_public_key_bytes = codecs.decode(network_bitcoin_public_key, 'hex')
	sha256_nbpk = hashlib.sha256(network_bitcoin_public_key_bytes)
	sha256_nbpk_digest = sha256_nbpk.digest()
	sha256_2_nbpk = hashlib.sha256(sha256_nbpk_digest)
	sha256_2_nbpk_digest = sha256_2_nbpk.digest()
	sha256_2_hex = codecs.encode(sha256_2_nbpk_digest, 'hex')
	checksum = sha256_2_hex[:8]
	address_hex = (network_bitcoin_public_key + checksum).decode('utf-8')
	address = base58(address_hex)

	## PUBLIC COMPD
	private_hex = codecs.decode(private, 'hex')
	# Get ECDSA public key
	key = ecdsa.SigningKey.from_string(private_hex, curve=ecdsa.SECP256k1).verifying_key
	key_bytes = key.to_string()
	key_hex = codecs.encode(key_bytes, 'hex')
	# Get X from the key (first half)
	key_string = key_hex.decode('utf-8')
	half_len = len(key_hex) // 2
	key_half = key_hex[:half_len]
	# Add bitcoin byte: 0x02 if the last digit is even, 0x03 if the last digit is odd
	last_byte = int(key_string[-1], 16)
	bitcoin_byte = b'02' if last_byte % 2 == 0 else b'03'
	public_key_comp = bitcoin_byte + key_half

	## PUBLIC COMPD ADDR
	public_comp_bytes = codecs.decode(public_key_comp, 'hex')
	sha256_bpk = hashlib.sha256(public_comp_bytes)
	sha256_bpk_digest = sha256_bpk.digest()
	ripemd160_bpk = hashlib.new('ripemd160')
	ripemd160_bpk.update(sha256_bpk_digest)
	ripemd160_bpk_digest = ripemd160_bpk.digest()
	ripemd160_bpk_hex = codecs.encode(ripemd160_bpk_digest, 'hex')
	network_byte = b'00'
	network_bitcoin_public_key = network_byte + ripemd160_bpk_hex
	network_bitcoin_public_key_bytes = codecs.decode(network_bitcoin_public_key, 'hex')
	sha256_nbpk = hashlib.sha256(network_bitcoin_public_key_bytes)
	sha256_nbpk_digest = sha256_nbpk.digest()
	sha256_2_nbpk = hashlib.sha256(sha256_nbpk_digest)
	sha256_2_nbpk_digest = sha256_2_nbpk.digest()
	sha256_2_hex = codecs.encode(sha256_2_nbpk_digest, 'hex')
	checksum = sha256_2_hex[:8]
	address_hex = (network_bitcoin_public_key + checksum).decode('utf-8')
	address_comp = base58(address_hex)

	## WIF IT!
	digest = hashlib.sha256(binascii.unhexlify('80' + private)).hexdigest()
	var = hashlib.sha256(binascii.unhexlify(digest)).hexdigest()
	var = binascii.unhexlify('80' + private + var[0:8])
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
	wif = chars[0] * pad + result

	return [private, wif, public, address, address_comp]