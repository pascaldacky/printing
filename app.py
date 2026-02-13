from flask import Flask, render_template, redirect, url_for
from models import db, Receipt, ReceiptItem
import config

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

# ---------- Routes ----------

@app.route('/')
def index():
    # List all receipts
    receipts = Receipt.query.all()
    return render_template('index.html', receipts=receipts)

@app.route('/create_test_receipt')
def create_test_receipt():
    last_receipt = Receipt.query.order_by(Receipt.id.desc()).first()
    next_number = f"R{int(last_receipt.receipt_no[1:]) + 1}" if last_receipt else "R1001"
    # Auto-generate a test receipt
    receipt = Receipt(receipt_no=next_number, subtotal=25.00, vat=2.50, total=27.50)
    db.session.add(receipt)
    db.session.commit()

    items = [
        ReceiptItem(receipt_id=receipt.id, name="Product A", quantity=1, price=5.00),
        ReceiptItem(receipt_id=receipt.id, name="Product B", quantity=2, price=10.00)
    ]
    db.session.add_all(items)
    db.session.commit()

    return redirect(url_for('show_receipt', receipt_id=receipt.id))

@app.route('/receipt/<int:receipt_id>')
def show_receipt(receipt_id):
    # Display receipt for phone
    receipt = Receipt.query.get_or_404(receipt_id)
    return render_template('receipt.html', receipt=receipt)

if __name__ == '__main__':
    app.run(debug=True)
