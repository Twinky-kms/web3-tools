import os

from web3 import Web3
from time import sleep
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

token_addresses = {
    'aArbWBTC': Web3.toChecksumAddress('0x078f358208685046a11c85e8ad32895ded33a249'),
    'aArbWETH': Web3.toChecksumAddress('0xe50fA9b3c56FfB159cB0FCA61F5c9D750e8128c8'),
}

network_rpc = os.getenv("NETWORK_RPC")
web3 = Web3(Web3.HTTPProvider(network_rpc, request_kwargs={'timeout': 60 }))
address = Web3.toChecksumAddress(os.getenv("WALLET_ADDRESS"))

def log(msg):
    debug = os.getenv("DEBUG")
    if debug:
        print(msg)

def get_eth_balance(address):
    balance = web3.eth.get_balance(address)
    return web3.fromWei(balance, 'ether')

def get_token_balance(address, token_address):
    abi = [{"constant":True,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"}]
    token_bal = web3.eth.contract(address=token_address, abi=abi).functions.balanceOf(address).call()
    return token_bal

def check_balance():
    csv_string = str(datetime.now()) + ',' + str(web3.eth.get_balance(address)) + ','
    for token in token_addresses:
        balance = get_token_balance(address, token_addresses[token])
        log(balance)
        csv_string += str(balance) + ','
    csv_string += ' \n'
    with open('balances.csv', 'a') as f:
        f.write(csv_string)

while True:
    check_balance()
    sleep(1800)
    