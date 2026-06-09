import json
from web3 import Web3
from solcx import compile_standard, install_solc

# Cài đặt phiên bản solc tương thích
install_solc("0.8.0")

with open("./contracts/ReviewVerification.sol", "r") as file:
    contract_source_code = file.read()

# Biên dịch mã nguồn Smart Contract sang mã máy EVM Bytecode và ABI
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {"ReviewVerification.sol": {"content": contract_source_code}},
    "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode.object"]}}}
}, solc_version="0.8.0")

bytecode = compiled_sol["contracts"]["ReviewVerification.sol"]["ReviewVerification"]["evm"]["bytecode"]["object"]
abi = compiled_sol["contracts"]["ReviewVerification.sol"]["ReviewVerification"]["abi"]

# Kết nối Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
admin_account = w3.eth.accounts[0]

# Khởi tạo tiến trình Deploy gốc bằng mã lệnh
ReviewContract = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = ReviewContract.constructor().transact({'from': admin_account})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"DEPLOY SUCCESSFUL!")
print(f"Contract Address: {tx_receipt.contractAddress}")
# Hãy copy địa chỉ in ra này thế chỗ vào phần CONTRACT_ADDRESS trong tệp backend/config.py