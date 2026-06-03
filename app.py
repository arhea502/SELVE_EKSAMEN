from flask import (Flask, render_template, redirect,
                   url_for, request, flash, jsonify, abort)

from flask_sqlalchemy import SQLAlchemy

from flask_login import (LoginManager, UserMixin,
                         login_user, logout_user,
                         login_required, current_user)

from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import markdown as md

app = Flask(__name__)

app.config['SECRET_KEY'] = '108158379'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

login_manager = LoginManager(app)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    is_admin = db.Colum(db.Boolean, default=False)
    ip_addresse = db.Column(db.String(50), nullable=True)

class Sections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)   
    topics = db.relationship('Topics', backref='section', lazy=True, cascade='all, delete-orphan')

class Topics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)   
 

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin'):
        db.session.add(User(
            username='admin',
            password_hash=generate_password_hash('admin123'),   
            is_admin=True
        ))
        db.session.commit()

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if not current_user.is_admin:   
            abort(403)
        return f(*args, **kwargs)
    return decorated

@app.route('/index', methods=['GET', 'POST'])
@admin_required
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if not user or not check_password_hash(user.password_hash, password_hash=request.form['password']).first():
