from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Initialize Flask App
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids unnecessary warnings

# Initialize Extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Flask-Migrate setup
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirects unauthorized users to login

# Import Routes (Fixed Circular Import)
from routes import *

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True,port = 5001)  # Auto-reloads when code changes
