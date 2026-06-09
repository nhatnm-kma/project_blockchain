// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title Hệ thống xác thực đánh giá sản phẩm Thương mại điện tử
 * @dev Tuân thủ nghiêm ngặt tiêu chuẩn định danh thực thể lớp Smart Contract ISO/IEC 23257
 */
contract ReviewVerification {
    
    address public admin;

    struct Review {
        address reviewer;
        uint256 rating;
        string comment;
        uint256 timestamp;
    }

    Review[] private reviews;
    mapping(address => bool) public approvedBuyers;

    event BuyerApproved(address indexed buyer);
    event ReviewSubmitted(address indexed reviewer, uint256 rating, string comment, uint256 timestamp);

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }

    constructor() {
        admin = msg.sender; // Tài khoản deploy khánh thành đóng vai trò Admin hệ thống
    }

    /**
     * @notice Xác thực quyền cho phép người mua hàng được đánh giá sản phẩm
     */
    function approveBuyer(address buyer) public onlyAdmin {
        require(buyer != address(0), "Invalid address");
        approvedBuyers[buyer] = true;
        emit BuyerApproved(buyer);
    }

    /**
     * @notice Đệ trình đánh giá sản phẩm lên mạng lưới phi tập trung
     */
    function submitReview(uint256 rating, string memory comment) public {
        // Ràng buộc bảo mật lõi chặn mọi hành vi xâm nhập từ tài khoản không được ủy quyền
        require(approvedBuyers[msg.sender], "Only verified buyers can review");
        require(rating >= 1 && rating <= 5, "Rating must be between 1 and 5");

        reviews.push(Review({
            reviewer: msg.sender,
            rating: rating,
            comment: comment,
            timestamp: block.timestamp
        }));

        emit ReviewSubmitted(msg.sender, rating, comment, block.timestamp);
    }

    /**
     * @notice Truy xuất danh sách toàn bộ đánh giá phục vụ tính minh bạch của hệ thống
     */
    function getReviews() public view returns (Review[] memory) {
        return reviews;
    }

    /**
     * @notice Kiểm tra trạng thái xác thực của tài khoản bất kỳ
     */
    function isApprovedBuyer(address user) public view returns (bool) {
        return approvedBuyers[user];
    }
}