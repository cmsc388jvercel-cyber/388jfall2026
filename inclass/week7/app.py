# app.py -- Week 7: the Parts Depot REST API (the textbook case study)
# No database today: parts live in a Python dict so we can focus on HTTP and REST.
from xml.etree import ElementTree as ET

from flask import Flask, Response, jsonify, request, session, url_for

app = Flask(__name__)
app.secret_key = "week7-demo-only"  # only used by the /visit route in Part 5

API_TOKEN = "demo-token"  # every write request must send: Authorization: Bearer demo-token

PARTS = {
    "00345": {"id": "00345", "name": "Hex bolt", "price": 0.25},
    "00346": {"id": "00346", "name": "Washer", "price": 0.10},
    "00347": {"id": "00347", "name": "Hex nut", "price": 0.15},
    "00348": {"id": "00348", "name": "Lock washer", "price": 0.12},
}
ORDERS = []  # a list of dicts; POST /orders appends to it


def part_view(part):
    """A representation of one part: its data plus a link to itself."""
    return {**part, "href": url_for("get_part", part_id=part["id"], _external=True)}


def wants_xml():
    return request.accept_mimetypes.best == "application/xml"


def xml_response(root):
    return Response(ET.tostring(root, encoding="unicode"), mimetype="application/xml")


def check_token():
    """Statelessness: the server remembers nothing about us, so every request must prove who it is."""
    return request.headers.get("Authorization") == f"Bearer {API_TOKEN}"


def unauthorized():
    return jsonify(error="missing or wrong Authorization header"), 401


@app.route("/")
def index():
    return jsonify(
        parts=url_for("list_parts", _external=True),
        orders=url_for("orders", _external=True),
    )


# ---- Part 3: GET the collection and one part -------------------------------------------------

@app.route("/parts")
def list_parts():
    if wants_xml():
        root = ET.Element("Parts")
        for part in PARTS.values():
            ET.SubElement(root, "Part", id=part["id"], href=part_view(part)["href"])
        return xml_response(root)
    return jsonify(parts=[{"id": p["id"], "href": part_view(p)["href"]} for p in PARTS.values()])


@app.route("/parts/<part_id>")
def get_part(part_id):
    part = PARTS.get(part_id)
    if part is None:
        return jsonify(error=f"no part {part_id}"), 404
    if wants_xml():
        view = part_view(part)
        root = ET.Element("Part", id=view["id"])
        ET.SubElement(root, "Name").text = view["name"]
        ET.SubElement(root, "Price").text = str(view["price"])
        ET.SubElement(root, "Link", rel="all-parts", href=url_for("list_parts", _external=True))
        return xml_response(root)
    return jsonify(**part_view(part), all_parts=url_for("list_parts", _external=True))


# ---- Part 4: PUT and DELETE are idempotent ---------------------------------------------------

@app.route("/parts/<part_id>", methods=["PUT"])
def put_part(part_id):
    if not check_token():
        return unauthorized()
    body = request.get_json(silent=True) or {}
    if "name" not in body or "price" not in body:
        return jsonify(error="send JSON with name and price"), 400
    created = part_id not in PARTS
    PARTS[part_id] = {"id": part_id, "name": body["name"], "price": body["price"]}
    return jsonify(**part_view(PARTS[part_id])), (201 if created else 200)


@app.route("/parts/<part_id>", methods=["DELETE"])
def delete_part(part_id):
    if not check_token():
        return unauthorized()
    if PARTS.pop(part_id, None) is None:
        return jsonify(error=f"no part {part_id}"), 404
    return "", 204


# ---- Part 3 and 4: POST creates something new every time -------------------------------------

@app.route("/orders", methods=["GET", "POST", "DELETE"])
def orders():
    if not check_token():
        return unauthorized()
    if request.method == "POST":
        body = request.get_json(silent=True) or {}
        if body.get("part_id") not in PARTS:
            return jsonify(error="part_id must be a real part"), 400
        order = {"id": len(ORDERS) + 1, "part_id": body["part_id"], "quantity": body.get("quantity", 1)}
        ORDERS.append(order)
        location = url_for("get_order", order_id=order["id"], _external=True)
        return jsonify(**order, href=location), 201, {"Location": location}
    if request.method == "DELETE":  # demo helper: wipe the collection between runs
        ORDERS.clear()
        return "", 204
    return jsonify(count=len(ORDERS), orders=ORDERS)


@app.route("/orders/<int:order_id>")
def get_order(order_id):
    if not check_token():
        return unauthorized()
    for order in ORDERS:
        if order["id"] == order_id:
            return jsonify(**order)
    return jsonify(error=f"no order {order_id}"), 404


# ---- Part 5: the opposite of stateless -------------------------------------------------------

@app.route("/visit")
def visit():
    """NOT RESTful on purpose: the count lives in a cookie the client has to keep sending."""
    session["count"] = session.get("count", 0) + 1
    return jsonify(visits=session["count"])


# ---- Part 6: logical URIs --------------------------------------------------------------------

@app.route("/catalog/<int:number>")
def catalog(number):
    """A million URLs and not one file: the representation is built when the request arrives."""
    if not 1 <= number <= 999_999:
        return jsonify(error="no such catalog number"), 404
    return jsonify(id=f"{number:06d}", name=f"Part #{number:06d}", price=round(0.05 + (number % 100) / 100, 2))


@app.errorhandler(404)
def not_found(error):
    return jsonify(error="not found"), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify(error="method not allowed", allowed=sorted(error.valid_methods or [])), 405
