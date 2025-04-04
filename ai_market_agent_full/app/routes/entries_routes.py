# app/routes/entries_routes.py
from flask import Blueprint, render_template
from app.db import db
from app.models import Entry, Source

entries_bp = Blueprint('entries', __name__)

@entries_bp.route('/entries')
def entries():
    all_entries = (
        db.session.query(Entry)
        .join(Source)
        .order_by(Entry.posted_at.desc())
        .limit(100)
        .all()
    )
    return render_template('entries.html', entries=all_entries)
