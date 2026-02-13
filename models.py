from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Receipt(db.Model):
    __tablename__ = 'receipts'
    id = db.Column(db.Integer, primary_key=True)
    receipt_no = db.Column(db.String(20), nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    vat = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    items = db.relationship('ReceiptItem', backref='receipt', cascade="all, delete-orphan")

class ReceiptItem(db.Model):
    __tablename__ = 'receipt_items'
    id = db.Column(db.Integer, primary_key=True)
    receipt_id = db.Column(db.Integer, db.ForeignKey('receipts.id'))
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
