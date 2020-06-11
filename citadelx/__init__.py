import os
from flask import Flask
from flask_login import LoginManager

def create_app():
	app = Flask(__name__, instance_relative_config=True)

	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
		SQLALCHEMY_DATABASE_URI='sqlite:///db.sqlite3',
		SQLALCHEMY_TRACK_MODIFICATIONS=False,
	)

	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	from . import database, auth, main
	db = database.db
	db.init_app(app)
	with app.app_context():
		db.create_all()


	loginManager = LoginManager()
	loginManager.login_view='auth.login'
	loginManager.init_app(app)

	@loginManager.user_loader
	def load_user(user_id):
		return database.user.query.get(int(user_id))

	app.register_blueprint(auth.auth)
	app.register_blueprint(main.main)

	return app