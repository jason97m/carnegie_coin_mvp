from solcx import compile_standard, install_solc
import json

install_solc("0.8.20")

with open("blockchain/CarnegieCoin.sol", "r") as f:
    source_code = f.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"CarnegieCoin.sol": {"content": source_code}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.20",
)

# Debug: print the compiled JSON
print(json.dumps(compiled_sol, indent=4))

# Save ABI
with open("blockchain/CarnegieCoin_abi.json", "w") as f:
    json.dump(
        compiled_sol["contracts"]["CarnegieCoin.sol"]["CarnegieCoin"]["abi"], f, indent=4
    )
