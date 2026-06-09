from flask import Flask, render_template, request, redirect, url_for, flash
from contract_service import ContractService
import time

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = "blockchain_secure_secret_key"

# Khởi tạo tầng kết nối dịch vụ
try:
    service = ContractService()
    print("Blockchain connection successful")
except Exception as e:
    print(f"Error connecting to Blockchain network: {e}")
    service = None


def get_mapped_accounts():
    """
    Ánh xạ 3 tài khoản đại diện cho:
    - Admin
    - Buyer
    - Attacker
    """

    if not service:
        return {
            "admin": "0x0000000000000000000000000000000000000000",
            "buyer": "0x0000000000000000000000000000000000000000",
            "attacker": "0x0000000000000000000000000000000000000000"
        }

    try:
        accounts = service.get_accounts()

        if len(accounts) < 3:
            return {
                "admin": "0x0000000000000000000000000000000000000000",
                "buyer": "0x0000000000000000000000000000000000000000",
                "attacker": "0x0000000000000000000000000000000000000000"
            }

        return {
            "admin": accounts[0],
            "buyer": accounts[1],
            "attacker": accounts[2]
        }

    except Exception as e:
        print(f"Account loading error: {e}")

        return {
            "admin": "0x0000000000000000000000000000000000000000",
            "buyer": "0x0000000000000000000000000000000000000000",
            "attacker": "0x0000000000000000000000000000000000000000"
        }


@app.route('/')
def index():
    return redirect(url_for('admin_page'))


@app.route('/admin', methods=['GET', 'POST'])
def admin_page():

    nodes = get_mapped_accounts()
    is_approved = False

    if service:
        try:
            is_approved = service.check_buyer_status(nodes['buyer'])
        except Exception as e:
            print(f"Buyer status check failed: {e}")

    if request.method == 'POST':

        if not service:
            flash("Blockchain service unavailable", "danger")
            return redirect(url_for('admin_page'))

        buyer_to_approve = request.form.get('buyer_address')

        try:
            receipt = service.approve_buyer(
                nodes['admin'],
                buyer_to_approve
            )

            flash(
                f"SUCCESS: Buyer approved. Block: {receipt['blockNumber']}",
                "success"
            )

        except Exception as e:
            flash(f"FAILED: {str(e)}", "danger")

        return redirect(url_for('admin_page'))

    return render_template(
        'admin.html',
        nodes=nodes,
        is_approved=is_approved
    )


@app.route('/buyer', methods=['GET', 'POST'])
def buyer_page():

    nodes = get_mapped_accounts()

    if request.method == 'POST':

        if not service:
            flash("Blockchain service unavailable", "danger")
            return redirect(url_for('buyer_page'))

        rating = request.form.get('rating')
        comment = request.form.get('comment')

        try:
            receipt = service.submit_review(
                nodes['buyer'],
                rating,
                comment
            )

            flash(
                f"SUCCESS: Review submitted. Block: {receipt['blockNumber']}",
                "success"
            )

        except Exception as e:
            flash(
                f"FAILED: {str(e)}",
                "danger"
            )

        return redirect(url_for('buyer_page'))

    return render_template(
        'buyer.html',
        nodes=nodes
    )


@app.route('/attacker', methods=['GET', 'POST'])
def attacker_page():

    nodes = get_mapped_accounts()

    if request.method == 'POST':

        if not service:
            flash("Blockchain service unavailable", "danger")
            return redirect(url_for('attacker_page'))

        rating = request.form.get('rating')
        comment = request.form.get('comment')

        try:
            receipt = service.submit_review(
                nodes['attacker'],
                rating,
                comment
            )

            flash(
                f"SUCCESS: Attack succeeded?! Block: {receipt['blockNumber']}",
                "success"
            )

        except Exception:
            flash(
                "FAILED: Transaction reverted. Only verified buyers can review.",
                "danger"
            )

        return redirect(url_for('attacker_page'))

    return render_template(
        'attacker.html',
        nodes=nodes
    )


@app.route('/reviews')
def reviews_page():

    reviews_list = []

    if service:
        try:
            reviews_list = service.fetch_all_reviews()
        except Exception as e:
            print(f"Review loading error: {e}")

    nodes = get_mapped_accounts()

    return render_template(
        'reviews.html',
        reviews=reviews_list,
        nodes=nodes
    )


@app.route('/compliance')
def compliance_page():
    return render_template('compliance.html')


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )