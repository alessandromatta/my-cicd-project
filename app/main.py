from flask import Flask, jsonify
import os
import redis
from datetime import datetime

app = Flask(__name__)

# Connect to Redis
try:
    redis_host = os.environ.get('REDIS_HOST', 'redis')
    redis_port = int(os.environ.get('REDIS_PORT', 6379))
    r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    r.ping()
    redis_available = True
except Exception as e:
    print(f"Redis connection failed: {e}")
    redis_available = False
    r = None

@app.route('/')
def home():
    if redis_available:
        try:
            count = r.incr('request_count')
            return jsonify({
                "message": "Hello from CI/CD Lab!",
                "status": "success",
                "request_count": count,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            return jsonify({
                "message": "Hello from CI/CD Lab!",
                "status": "success (Redis unavailable)",
                "error": str(e)
            })
    else:
        return jsonify({
            "message": "Hello from CI/CD Lab!",
            "status": "success (no Redis)"
        })

@app.route('/health')
def health():
    redis_status = "connected" if redis_available else "disconnected"
    return jsonify({
        "status": "healthy",
        "redis": redis_status
    }), 200

@app.route('/api/data')
def get_data():
    return jsonify({"data": [1, 2, 3, 4, 5], "count": 5})

@app.route('/reset')
def reset():
    if redis_available:
        r.set('request_count', 0)
        return jsonify({"message": "Counter reset", "count": 0})
    return jsonify({"message": "Redis not available"}), 503

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)