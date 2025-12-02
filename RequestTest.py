from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()

url = "https://eth-sepolia.g.alchemy.com/v2/Ls_6CsWMq73LBpIud2B4v"
w3 = Web3(Web3.HTTPProvider(url))
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
print(CONTRACT_ADDRESS)
print("Connected:", w3.is_connected())
print("Chain:", w3.eth.chain_id)
print("Latest block:", w3.eth.block_number)
contract_address = Web3.to_checksum_address(CONTRACT_ADDRESS)
# Get code at the contract address
code = w3.eth.get_code(contract_address)
print("Contract code:", code.hex())

# Optional: Check if this is actually a deployed contract
if code == b'':  # or code.hex() == '0x'
    print("⚠️ This address is NOT a deployed contract on this network!")
else:
    print("✅ This is a deployed contract!")
