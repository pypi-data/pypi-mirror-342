from web3 import Web3
from solana.rpc.api import Client




def validate_eth_endpoint(from_private_key, rpc_url):
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    if not web3.is_connected():
        raise ConnectionError("Failed to connect to eth RPC node!")
    

    

def validate_bsc_endpoint(from_private_key, rpc_url):
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    if not web3.is_connected():
        raise ConnectionError("Failed to connect to bsc RPC node!")
    



def validate_sol_endpoint(from_private_key, rpc_url):
    client = Client(rpc_url)
    if not client.is_connected():
        raise ConnectionError("Failed to connect to sol RPC node!")     
