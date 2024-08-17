from flask import Flask
from app.data_services import db, init_db
from app.routes import routes_bp
from app.config import DATABASE_CONFIG

app = Flask(__name__)

# Configuring the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@"
    f"{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
)

init_db(app)

app.register_blueprint(routes_bp)
