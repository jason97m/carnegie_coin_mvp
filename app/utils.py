import os
from web3 import Web3
from dotenv import load_dotenv
import json

load_dotenv()  # loads .env variables

WEB3_PROVIDER = os.getenv("WEB3_PROVIDER")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
ACCOUNT_ADDRESS = os.getenv("ACCOUNT_ADDRESS")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")  # fill after deploying

w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER))

# Load compiled contract ABI
def load_contract_abi():
    with open("blockchain/CarnegieCoin_abi.json") as f:
        return json.load(f)

abi = load_contract_abi()
contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)


def get_balance(address=ACCOUNT_ADDRESS):
    """Returns the token balance of the given address."""
    try:
        balance = contract.functions.balanceOf(Web3.to_checksum_address(address)).call()
        # assuming 18 decimals for ERC20 token
        return balance / 10**18
    except Exception as e:
        print("Error fetching balance:", e)
        return None

def get_transfer_events():
    w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER")))
    contract_address = os.getenv("CONTRACT_ADDRESS")

    with open("blockchain/CarnegieCoin_abi.json") as f:
        abi = json.load(f)

    contract = w3.eth.contract(address=contract_address, abi=abi)

    # Fetch events
    transfer_filter = contract.events.Transfer.create_filter(fromBlock=0)
    events = transfer_filter.get_all_entries()

    parsed = []
    for e in events:
        parsed.append({
            "from": e['args']['from'],
            "to": e['args']['to'],
            "amount": e['args']['value'],
            "tx_hash": e['transactionHash'].hex(),
            "block": e['blockNumber']
        })

    return parsed
