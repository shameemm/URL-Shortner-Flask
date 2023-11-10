import os
import hashlib
from flask import Flask, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(255), unique=True, nullable=False)
    short_code = db.Column(db.String(8), unique=True, nullable=False)
    hits = db.Column(db.Integer, default=0)

    def __init__(self, long_url, short_code):
        self.long_url = long_url
        self.short_code = short_code
        self.hits = 0


def generate_short_code(long_url):
    # Generate a unique short code using the SHA-256 hash of the long URL
    hash_object = hashlib.sha256(long_url.encode())
    return hash_object.hexdigest()[:8]


@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form.get('long_url')

    if long_url:
        short_code = generate_short_code(long_url)
        new_url = URL(long_url=long_url, short_code=short_code)
        db.session.add(new_url)
        db.session.commit()

        short_url = f'http://localhost:5000/{short_code}'
        return jsonify({'short_url': short_url}), 201
    else:
        return jsonify({'error': 'Missing long_url parameter'}), 400


@app.route('/<short_code>')
def redirect_to_original(short_code):
    url = URL.query.filter_by(short_code=short_code).first()

    if url:
        url.hits += 1
        db.session.commit()
        return redirect(url.long_url, code=302)
    else:
        return jsonify({'error': 'Short URL not found'}), 404


@app.route('/metadata/<short_code>')
def get_metadata(short_code):
    url = URL.query.filter_by(short_code=short_code).first()

    if url:
        metadata = {
            'short_url': f'http://localhost:5000/{short_code}',
            'long_url': url.long_url,
            'hits': url.hits
        }
        return jsonify(metadata)
    else:
        return jsonify({'error': 'Short URL not found'}), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)