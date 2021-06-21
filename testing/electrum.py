#from bitcoinlib.mnemonic import Mnemonic
import bitcoinlib

words = bitcoinlib.mnemonic.Mnemonic().generate()
key = bitcoinlib.keys.HDKey().from_passphrase(words)
print(key)
print(key.public())
print(key.address())
print(key.address_uncompressed())