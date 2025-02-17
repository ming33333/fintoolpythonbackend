from flask import Flask
from dotenv import load_dotenv
import os
from app.routes import main as main_blueprint

# Load environment variables from .env file
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Register blueprints
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)