from web3 import Web3
from config import Config

class ContractService:
    def __init__(self):
        # Kết nối tới DLT Layer (Ganache)
        self.w3 = Web3(Web3.HTTPProvider(Config.GANACHE_URL))
        if not self.w3.is_connected():
            raise Exception("Cannot connect to Ganache network RPC endpoint")
        
        # Khởi tạo instance Smart Contract qua ABI và Contract Address
        self.contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(Config.CONTRACT_ADDRESS),
            abi=Config.CONTRACT_ABI
        )

    def get_accounts(self):
        return self.w3.eth.accounts

    def approve_buyer(self, admin_address, buyer_address):
        # Admin thực hiện ký giao dịch phê duyệt phân quyền
        tx_hash = self.contract.functions.approveBuyer(
            Web3.to_checksum_address(buyer_address)
        ).transact({'from': Web3.to_checksum_address(admin_address)})
        
        # Chờ đợi biên lai xác nhận khối từ blockchain
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    def submit_review(self, sender_address, rating, comment):
        # Hàm xử lý gửi review lên chuỗi khối
        tx_hash = self.contract.functions.submitReview(
            int(rating), comment
        ).transact({'from': Web3.to_checksum_address(sender_address)})
        
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    def fetch_all_reviews(self):
        raw_reviews = self.contract.functions.getReviews().call()
        formatted_reviews = []
        for index, item in enumerate(raw_reviews):
            # Lấy thông tin khối để hiển thị chi tiết Transaction Hash phục vụ minh chứng
            formatted_reviews.append({
                "reviewer": item[0],
                "rating": item[1],
                "comment": item[2],
                "timestamp": item[3]
            })
        return formatted_reviews

    def check_buyer_status(self, user_address):
        return self.contract.functions.isApprovedBuyer(Web3.to_checksum_address(user_address)).call()