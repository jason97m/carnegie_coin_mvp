from web3 import Web3
from dotenv import load_dotenv
import json
import os
import requests

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

#def get_transfer_events(start_block=0, end_block=None):
#    """
#    Fetch Transfer events emitted by CarnegieCoin.
#    """
#    if end_block is None:
#        end_block = w3.eth.get_block_number()
#
#    transfer_event = contract.events.Transfer()
#
#    logs = transfer_event.get_logs(from_block=start_block, to_block=end_block)
#
#    event_list = []
#    for log in logs:
#        event_list.append({
#            "from": log["args"]["from"],
#            "to": log["args"]["to"],
#            "value": log["args"]["value"],
#            "tx_hash": log["transactionHash"].hex()
#        })

#    return event_list


#def get_transfer_events(start_block=0, end_block="latest"):
#    if end_block == "latest":
#        end_block = w3.eth.block_number

    # Event signature hash for ERC-20 Transfer
#    transfer_topic = w3.keccak(text="Transfer(address,address,uint256)").hex()

#    filter_params = {
#        "fromBlock": start_block,
#        "toBlock": end_block,
#        "address": CONTRACT_ADDRESS,
#        "topics": [transfer_topic],
#    }

#    print("DEBUG filter_params:", filter_params)

#    try:
#        logs = w3.eth.get_logs(filter_params)
#    except Exception as e:
#        print("\n RPC ERROR DETAILS ")
#        print(type(e), str(e))
#        raise

#    events = []
#    for log in logs:
#        decoded = contract.events.Transfer().process_log(log)
#        events.append({
#            "from": decoded["args"]["from"],
#            "to": decoded["args"]["to"],
#            "value": decoded["args"]["value"],
#            "tx_hash": log["transactionHash"].hex(),
#        })

#    return events

# Function to get Transfer events
def get_transfer_events(start_block=None, end_block=None):
    if not w3.is_connected():
        raise ConnectionError("Web3 provider not connected.")

    # Set default block range if not provided
    if start_block is None:
        start_block = w3.eth.block_number - 5000  # last 5000 blocks by default
    if end_block is None:
        end_block = w3.eth.block_number

    # Prepare the event object and topic
    transfer_event = contract.events.Transfer
    transfer_topic = Web3.keccak(text="Transfer(address,address,uint256)").hex()

    # Build filter parameters
    filter_params = {
        "fromBlock": start_block,
        "toBlock": end_block,
        "address": CONTRACT_ADDRESS,
        "topics": [transfer_topic],
    }

    # Fetch logs
    try:
        logs = w3.eth.get_logs(filter_params)
    except Exception as e:
        print("Error fetching logs:", e)
        return []

    # Decode logs
    events = []
    for log in logs:
        decoded = transfer_event().process_log(log)
        events.append({
            "from": decoded["args"]["from"],
            "to": decoded["args"]["to"],
            "value": decoded["args"]["value"],
            "tx_hash": decoded["transactionHash"].hex(),
            "block": log["blockNumber"]
        })

    # Sort newest first
    events.sort(key=lambda x: x["block"], reverse=True)
    return events
