from pathlib import Path
import os

from flask_assets import Bundle

BASE_DIR = Path(__file__).resolve().parent.parent
ALLOWED_EXTENSIONS = ("png", "jpeg", "jpg", "gif", "txt", "pdf", "md", "json")

def get_env_vars(name, default):
    env = os.getenv(name)
    if env is None:
        if default is None:
            raise ValueError("Ne peut être vide.")
        return default
    return env


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


css = Bundle(
    "css/src/main.css",
    "css/src/navbar.css",
    "css/src/forms.css",
    "css/src/messages.css",
    "css/src/pagination.css",
    "css/src/dropdown.css",
    "css/src/posts.css",
    "css/src/about.css",
    "css/src/footer.css",
    output="css/dist/main.min.css"
)

js = Bundle(
    "js/src/main.js",
    "js/src/navbar.js",
    "js/src/dropdown.js",
    output="js/dist/main.min.js"
)