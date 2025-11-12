import os
from flask import Flask
from routes.booking_routes import booking_bp
from routes.admin_routes import eta_history_bp
from routes.route_admin_routes import route_admin_bp
from models.shipment_model import init_db
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "defaultsecret")
app.register_blueprint(eta_history_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(route_admin_bp)

init_db()

if __name__ == "__main__":
    app.run(port=5000, debug=True)