## Redis Caching Demo

### Setup

1. Install everything in `requirements.txt`. Install `redis` and `redis-server`. Instructions depend on OS.

2. Run `redis-server` to run a Redis server.

3. Run `python3 app.py` to run a Flask server.

### Operation

Example POST requests:

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"name":"apple"}' http://localhost:5000/items
```
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"name":"banana"}' http://localhost:5000/items
```

`GET` request:

```bash
curl http://localhost:5000/items
```

### Credits

Original code, used with revisions: https://medium.com/@fahadnujaimalsaedi/using-flask-and-redis-to-optimize-web-application-performance-34a8ae750097 

