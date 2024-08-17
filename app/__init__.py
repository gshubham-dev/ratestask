from flask import Flask
from app.data_services import db, init_db
from app.routes import routes_bp
from app.config import DATABASE_CONFIG

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@"
    f"{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
)

# Initialize the database connection
init_db(app)

# Register the application blueprint for routing
app.register_blueprint(routes_bp)

# Entry point for running the application
if __name__ == '__main__':
    app.run(debug=True)