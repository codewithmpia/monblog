from pathlib import Path
import os
import requests

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


def send_sms(msg):
    user_id = get_env_vars("SMS_USER_ID", "codewithmpia")
    api_key = get_env_vars("SMS_API_KEY", "top-secret")

    url = f"https://smsapi.free-mobile.fr/sendmsg?user={user_id}&pass={api_key}&msg={msg}"

    req = requests.post(url)

    if req.status_code != 200:
        pass
    return f"Message envoyé avec success!, {req.status_code}"


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
    filters=["cssmin"],
    output="css/dist/main.min.css"
)

js = Bundle(
    "js/src/main.js",
    "js/src/navbar.js",
    "js/src/dropdown.js",
    filters=["jsmin"],
    output="js/dist/main.min.js"
)

