from flask import Flask, jsonify, request
from flask_caching import Cache
import redis

# application config
app = Flask(__name__)
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0

# flask-caching config
cache = Cache(app)
cache.init_app(app)

# redis config
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# "database" config
items = []
next_id = 1

@app.route("/items", methods=["POST"])
def add_item():
    global next_id

    data = request.get_json() or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": "Missing 'name'"}), 400

    item = {"id": next_id, "name": name}
    items.append(item)
    next_id += 1

    # cache invalidation
    cache.delete_memoized(get_items)
    print("[LOG] Cache invalidated.")

    return jsonify({"message": "Item added", "item": item}), 201

# cached route - only runs when cache misses
@app.route("/items", methods=["GET"])
@cache.cached(timeout=10) # TTL setting
def get_items():
    print("[LOG] Cache missed.")
    return jsonify(items)

if __name__ == '__main__':
    app.run(debug=True)