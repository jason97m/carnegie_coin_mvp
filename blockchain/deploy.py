from web3 import Web3

provider_url = "https://eth-sepolia.g.alchemy.com/v2/Ls_6CsWMq73LBpIud2B4v"
w3 = Web3(Web3.HTTPProvider(provider_url))

print("Connected:", w3.is_connected())
print("Chain ID:", w3.eth.chain_id)  # 11155111 = Sepolia
