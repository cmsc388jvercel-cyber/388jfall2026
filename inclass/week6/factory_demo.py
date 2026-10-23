# factory_demo.py -- Week 6, Part 2: two apps from one factory.
# Runs without Mongo running: python3 factory_demo.py
import os
os.environ.setdefault("MONGO_URI", "mongodb://localhost/week6")

from flask_app import create_app

dev_app = create_app({"SITE_NAME": "Week 6 (dev)", "DEBUG": True})
test_app = create_app({"SITE_NAME": "Week 6 (testing)", "TESTING": True})

print(dev_app.config["SITE_NAME"], "| debug:", dev_app.config["DEBUG"])
print(test_app.config["SITE_NAME"], "| testing:", test_app.config["TESTING"])
print("same object?", dev_app is test_app)
print()
print(dev_app.url_map)
