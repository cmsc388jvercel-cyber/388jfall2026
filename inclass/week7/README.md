# Week 7 in-class demo: HTTP and REST APIs (the Parts Depot case study)

One small Flask API (`app.py`) that follows the Parts Depot example from the textbook's REST page, plus five tiny client scripts, one per part of the lecture. There is **no database today**: parts and orders live in Python variables, so restarting the server resets everything. Uses the same Flask 2.0.3 pins as the Week 5 and Week 6 demos (and the P4 starter), plus `requests`. Use a **new virtual environment** and Python 3.10 to 3.12.

## Files

- `app.py`: the API. `GET /parts`, `GET /parts/<id>`, `PUT /parts/<id>`, `DELETE /parts/<id>`, `GET`/`POST /orders`, plus two extra routes: `/visit` (a cookie counter, the opposite of stateless) and `/catalog/<n>` (a million logical URLs, no files).
- `raw_http_demo.py`: sends hand-typed HTTP over a plain socket and prints the raw reply (Part 1).
- `get_demo.py`: GET the list, follow the links, then ask for XML with the `Accept` header (Part 3).
- `idempotency_demo.py`: retries `POST`, `PUT` and `DELETE` twice and compares the results (Part 4).
- `stateless_demo.py`: the `Authorization` header on every request, and the cookie-based `/visit` counter (Part 5).
- `uri_demo.py`: requests three catalog URLs and shows there are no matching files (Part 6).
- `.flaskenv`: Flask settings (port 5007). It is not tracked by git (see `.gitignore`), so create it yourself from the block below if it is missing.

```text
FLASK_APP=app.py
FLASK_DEBUG=1
FLASK_RUN_PORT=5007
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

No `.env` file is needed this week.

## Run

Terminal 1, the server:

```bash
flask run
```

Terminal 2, the same folder with the venv active, run the demos in this order:

```bash
python3 raw_http_demo.py
python3 get_demo.py
python3 idempotency_demo.py
python3 stateless_demo.py
python3 uri_demo.py
```

The server keeps its data in memory, so `idempotency_demo.py` changes part `00345` and deletes then restores part `00348`. Stop and restart `flask run` to get back to the starting data before running the demos again.

## curl cheat sheet

```bash
curl -i http://localhost:5007/parts/00345
curl -v http://localhost:5007/parts/00345
curl -H "Accept: application/xml" http://localhost:5007/parts
curl -i -X POST http://localhost:5007/orders -H "Authorization: Bearer demo-token" -H "Content-Type: application/json" -d '{"part_id": "00346", "quantity": 3}'
curl -i -X DELETE http://localhost:5007/parts/00347 -H "Authorization: Bearer demo-token"
```

## Notes

- Write requests need the header `Authorization: Bearer demo-token`. That is a made-up token for this demo, not a real secret.
- `python-dotenv` is in `requirements.txt` on purpose: it is what lets `flask run` read `.flaskenv` and start on port 5007 instead of 5000.
- The dev server answers with `HTTP/1.0` (the Werkzeug 2.0.3 default). Real servers answer with 1.1 or later.
- P3 calls the OMDb API with `requests`, just like these scripts call our own API. The app itself is separate from P3.
