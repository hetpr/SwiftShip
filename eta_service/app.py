from flask import Flask
from routes.eta_routes import eta_bp

app = Flask(__name__)
app.register_blueprint(eta_bp)

if __name__ == "__main__":
    app.run(port=5001, debug=True)