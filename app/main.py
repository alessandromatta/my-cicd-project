from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Hello from CI/CD Lab!", "status": "success"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/data')
def get_data():
    return jsonify({"data": [1, 2, 3, 4, 5], "count": 5})

if __name__ == '__main__':
    # Use environment variable for debug mode, default to False for production
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)