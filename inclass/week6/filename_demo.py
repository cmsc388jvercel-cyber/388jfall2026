# filename_demo.py -- Week 6, Part 4: never trust the filename the browser sends.
# Runs on its own: python3 filename_demo.py
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploads"

for name in ["cat.png", "my cat photo.png", "../../etc/passwd", "../app.py", "résumé.png"]:
    safe = secure_filename(name)
    print(f"{name!r:24} -> {safe!r:20} saved at {os.path.join(UPLOAD_FOLDER, safe)}")
