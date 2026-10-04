import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-12345')

# Uses local SQLite database when running on your machine
db_url = os.getenv('DATABASE_URL', 'sqlite:///messages.db')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html', name="Daylon Rock")

@app.route('/submit', methods=['POST'])
def submit_message():
    sender_name = request.form.get('sender_name')
    email = request.form.get('email')
    content = request.form.get('content')

    if sender_name and email and content:
        new_msg = Message(sender_name=sender_name, email=email, content=content)
        db.session.add(new_msg)
        db.session.commit()
        flash('Thank you! Your message has been received.', 'success')
    else:
        flash('Please fill in all required fields.', 'error')

    return redirect(url_for('home'))

@app.route('/admin/messages')
def view_messages():
    admin_key = os.getenv('ADMIN_KEY', 'admin123')
    provided_key = request.args.get('key')

    if provided_key != admin_key:
        return "Unauthorized Access", 401

    messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template('admin.html', messages=messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)