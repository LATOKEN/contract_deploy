import asyncio
import configparser
import os
import time
import web3
import ethereum


FEED_PRIVATE_KEY = bytes.fromhex('d95d6db65f3e2223703c5d8e205d98e3e6b470f067b0f94f6c6bf73d4301ce48')
CHAIN_ID = 41
LOCALNET_NODE = 'http://127.0.0.1:7070'
DEVNET_NODE = 'http://88.99.87.58:7070'
TESTNET_NODE = 'http://95.217.17.248:7070'


class Wallet:
    def __init__(self, private_key, connection):
        self.private_key = private_key
        self.address = ethereum.utils.checksum_encode(ethereum.utils.privtoaddr(self.private_key))
        self.connection = connection
        self.nonce = self.connection.eth.getTransactionCount(self.address)

    def send(self, to, amount):
        transaction = {
            'from': self.address,
            'to': to,
            'value': amount,
            'gas': 4000000,
            'gasPrice': 1,
            'nonce': self.nonce,
            'chainId': CHAIN_ID
        }
        signed = web3.eth.Account.signTransaction(transaction, self.private_key)
        txid = self.connection.eth.sendRawTransaction(signed.rawTransaction)
        self.nonce += 1
        return txid

    def tx_info(self, txid):
        return self.connection.eth.getTransactionReceipt(txid)

    def update_nonce(self):
        self.nonce = self.connection.eth.getTransactionCount(self.address)

    def deploy_contract(self, bytecode, abi):
        contract = self.connection.eth.contract(bytecode=bytecode,  abi=abi)
        print(contract.all_functions())
        tx = contract.constructor().buildTransaction({'from': self.address, "nonce": self.nonce, "gasPrice": 1})
        signed = web3.eth.Account.signTransaction(tx, self.private_key)
        txid = bytes.hex(self.connection.eth.sendRawTransaction(signed.rawTransaction))
        tx_receipt = self.connection.eth.wait_for_transaction_receipt(txid)
        return tx_receipt.contractAddress

    def totalSupply(self, contract_address, abi):
        contract = self.connection.eth.contract(address=contract_address, abi=abi)
        return contract.functions.totalSupply().call()
    
    def allowance(self, contract_address, abi, owner, spender):
        contract = self.connection.eth.contract(address=contract_address, abi=abi)
        return contract.functions.allowance(owner, spender).call()
    
    def init(self, contract_address, abi):
        contract = self.connection.eth.contract(address=contract_address, abi=abi)
        return contract.functions.init().call()

    def owner(self, contract_address, abi):
        contract = self.connection.eth.contract(address=contract_address, abi=abi)
        return contract.functions.original().call()

    def createPool(self, contract_address, abi, token0, token1, fee):
        contract = self.connection.eth.contract(address=contract_address, abi=abi)
        return contract.functions.createPool(token0, token1, fee).call()
    
    def mint_larc20(self, contract_address, abi, receiver_address, amount):
        contract = self.connection.eth.contract(address=contract_address, abi=abi)
        tx = contract.functions.mint(receiver_address,  amount).buildTransaction({'from': self.address, "nonce": self.nonce, "gasPrice": 1})
        signed = web3.eth.Account.signTransaction(tx, self.private_key)
        txid = bytes.hex(self.connection.eth.sendRawTransaction(signed.rawTransaction))
        tx_receipt = self.connection.eth.wait_for_transaction_receipt(txid)

    def increase_allowance_larc20(self, contract_address, abi, address, amount):
        contract = self.connection.eth.contract(address=contract_address, abi=abi)
        tx = contract.functions.increaseAllowance(address,  amount).buildTransaction({'from': self.address, "nonce": self.nonce, "gasPrice": 1})
        signed = web3.eth.Account.signTransaction(tx, self.private_key)
        txid = bytes.hex(self.connection.eth.sendRawTransaction(signed.rawTransaction))
        tx_receipt = self.connection.eth.wait_for_transaction_receipt(txid)

    def balance_of_larc20(self, contract_address, abi, address):
        contract = self.connection.eth.contract(address=contract_address, abi=abi)
        return contract.functions.balanceOf(address).call()

    def transfer_larc20(self, contract_address, abi, receiver_address, amount):
        contract = self.connection.eth.contract(address=contract_address, abi=abi)
        print(contract.all_functions())
        tx = contract.functions.transfer(receiver_address,  amount).buildTransaction({'from': self.address, "nonce": self.nonce, "gasPrice": 1})
        print(tx)
        signed = web3.eth.Account.signTransaction(tx, self.private_key)
        print(signed)
        txid = bytes.hex(self.connection.eth.sendRawTransaction(signed.rawTransaction))
        print(txid)
        tx_receipt = self.connection.eth.wait_for_transaction_receipt(txid)
    
if __name__ == '__main__':
    with open("UniswapV3Factory.abi", "r") as abifile:
        abi = abifile.read()
    with open("UniswapV3Factory.wasm", "rb") as wasmfile:
        bytecode = bytes.hex(wasmfile.read())
    
    node = web3.Web3(web3.Web3.HTTPProvider(DEVNET_NODE))
    feed_wallet = Wallet(FEED_PRIVATE_KEY, node)
    result = feed_wallet.deploy_contract(bytecode, abi)

    print(result)
