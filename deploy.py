import json
import subprocess
from web3 import Web3

SOLC_PATH = r"C:\Users\khang\Downloads\App\solc.exe"

# Compile contract bằng solc.exe
result = subprocess.run(
    [
        SOLC_PATH,
        "--combined-json",
        "abi,bin",
        "contracts/ReviewVerification.sol"
    ],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print(result.stderr)
    raise Exception("Compile failed")

compiled = json.loads(result.stdout)

contract_key = "contracts/ReviewVerification.sol:ReviewVerification"

# Debug nếu cần
print("Contracts found:")
print(compiled["contracts"].keys())

# Lấy ABI và Bytecode
abi = compiled["contracts"][contract_key]["abi"]
bytecode = compiled["contracts"][contract_key]["bin"]

# Kết nối Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

if not w3.is_connected():
    raise Exception("Cannot connect to Ganache")

admin_account = w3.eth.accounts[0]

print("Connected to Ganache")
print("Admin account:", admin_account)

# Deploy contract
ReviewContract = w3.eth.contract(
    abi=abi,
    bytecode=bytecode
)

tx_hash = ReviewContract.constructor().transact({
    "from": admin_account
})

print("Transaction hash:", tx_hash.hex())

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("\nDEPLOY SUCCESSFUL!")
print("Contract Address:", tx_receipt.contractAddress)