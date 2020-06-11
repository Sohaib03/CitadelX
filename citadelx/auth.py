from flask import Blueprint, render_template, redirect, url_for, request,flash
from werkzeug.security import generate_password_hash, check_password_hash
from .database import db, user
from flask_login import login_user, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
	return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
	email = request.form.get('email')
	password = request.form.get('password')
	remember = True if request.form.get('remember') else False

	target = user.query.filter_by(email=email).first()
	if not target or not check_password_hash(target.password, password):
		flash('Please check your login credentials')
		return redirect(url_for('auth.login'))


	login_user(target, remember=remember)
	return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
	return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
	email = request.form.get('email')
	name = request.form.get('name')
	password = request.form.get('password')

	if user.query.filter_by(email=email).first():
		flash('Email aready exists.')
		return redirect(url_for('auth.signup')) 

	elif user.query.filter_by(username=name).first():
		flash('Username taken.')
		return redirect(url_for('auth.signup'))

	new_user = user(name, email, generate_password_hash(password, method='sha256'))
	db.session.add(new_user)
	db.session.commit()

	return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.index'))

