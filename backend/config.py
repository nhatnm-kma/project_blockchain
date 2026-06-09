import os

class Config:
    # URL kết nối RPC tới mạng Ganache cục bộ
    GANACHE_URL = "http://127.0.0.1:7545"
    
    # Địa chỉ Smart Contract sau khi deploy (sẽ cập nhật sau khi chạy deploy)
    CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3" 
    
    # Định dạng mã tóm tắt giao diện nhị phân ABI (Sẽ được sinh tự động hoặc điền thủ công)
    CONTRACT_ABI = [
	{
		"anonymous": False,
		"inputs": [
			{"indexed": True, "internalType": "address", "name": "buyer", "type": "address"}
		],
		"name": "BuyerApproved",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{"indexed": True, "internalType": "address", "name": "reviewer", "type": "address"},
			{"indexed": False, "internalType": "uint256", "name": "rating", "type": "uint256"},
			{"indexed": False, "internalType": "string", "name": "comment", "type": "string"},
			{"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"}
		],
		"name": "ReviewSubmitted",
		"type": "event"
	},
	{
		"inputs": [{"internalType": "address", "name": "buyer", "type": "address"}],
		"name": "approveBuyer",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getReviews",
		"outputs": [
			{
				"components": [
					{"internalType": "address", "name": "reviewer", "type": "address"},
					{"internalType": "uint256", "name": "rating", "type": "uint256"},
					{"internalType": "string", "name": "comment", "type": "string"},
					{"internalType": "uint256", "name": "timestamp", "type": "uint256"}
				],
				"internalType": "struct ReviewVerification.Review[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [{"internalType": "address", "name": "user", "type": "address"}],
		"name": "isApprovedBuyer",
		"outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{"internalType": "uint256", "name": "rating", "type": "uint256"},
			{"internalType": "string", "name": "comment", "type": "string"}
		],
		"name": "submitReview",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]