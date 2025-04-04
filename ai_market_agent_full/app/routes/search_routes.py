from flask import Blueprint, render_template, request
from app.db import db
from app.models import Entry, Source

# změněný název blueprintu:
search_bp = Blueprint('search_bp', __name__)

@search_bp.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    query = ''
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            results = (
                db.session.query(Entry)
                .join(Source)
                .filter(
                    Entry.title.ilike(f"%{query}%") |
                    Entry.content.ilike(f"%{query}%")
                )
                .order_by(Entry.posted_at.desc())
                .limit(50)
                .all()
            )
    return render_template('search.html', query=query, results=results)
