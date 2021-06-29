# Plutus Bitcoin Brute Forcer

A Bitcoin wallet collider that brute forces wallet addresses

## About This Fork

Using a June 9th 2021 database from [AnasMK9's fork](https://github.com/AnasMK9/Plutus), and pruned the git history to reduce repo size.

- `run_bruteforce.py` - random keys generated with [Plutus-Scroo](https://github.com/franzkruhm/Plutus-Scroo)'s keygen. Original keygen is present but unused.
- `run_mnemonic.py` - addresses of wallets generated using [bitcoinlib](https://pypi.org/project/bitcoinlib/) based on a mnemonic strings.
- `run_flood.py` - picks an inital random seed, and then checks neighboring seeds sequentially in both positive and negative direction.
- _todo_ - make flood algorithm which resets and picks a new starting seed after every N iterations.

## Running the scripts

```bash
$ sudo apt -y install git-all
$ sudo apt -y install python3-pip
$ sudo apt -y install libgmp3-dev
$ git clone https://github.com/swift502/Plutus.git
$ cd Plutus
$ pip3 install -r requirements.txt
$ pip3 install ecdsa
```

Then either one of these:

```bash
$ python3 run_bruteforce.py
$ python3 run_flood.py
$ python3 run_mnemonic.py
```

`ecdsa` should probably just be in the requirements.txt file. Todo.
