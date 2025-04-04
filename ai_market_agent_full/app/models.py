from app.db import db
from datetime import datetime

class Source(db.Model):
    __tablename__ = 'sources'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(500))
    entries = db.relationship('Entry', back_populates='source')

class Entry(db.Model):
    __tablename__ = 'entries'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted_at = db.Column(db.DateTime, nullable=False)
    source_id = db.Column(db.Integer, db.ForeignKey('sources.id'))
    source = db.relationship('Source', back_populates='entries')

class ProductEntry(db.Model):
    __tablename__ = 'product_entries'

    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    brand = db.Column(db.String, nullable=True)
    price = db.Column(db.Float, nullable=True)
    reviews_count = db.Column(db.Integer, nullable=True)
    image_url = db.Column(db.String, nullable=True)
    product_url = db.Column(db.String, nullable=False)
    scraped_at = db.Column(db.DateTime, default=datetime.utcnow)
