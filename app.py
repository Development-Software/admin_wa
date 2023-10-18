from flask import Flask, render_template, session, request
from functions.db.invite import validate_confirm
from functions.automatic_api.send_api import get_url_invite
from routes.auth import auth_bp

app = Flask(__name__, static_url_path="/static")
app.secret_key = "mysecretkey"
app.config["DEBUG"] = True
app.register_blueprint(auth_bp)


@app.route("/")
def index():
    return render_template("html/login.html")


@app.route("/post_confirm/<id>")
def post_confirm(id):
    confirmed = validate_confirm(id)
    if confirmed:
        url = get_url_invite(id)
    else:
        url = "https://xvivonne.com/"
    return render_template("html/post_invite.html", confirmed=confirmed, url=url)


@app.route("/control")
def control():
    return render_template("html/login.html")


if __name__ == "__main__":
    app.run()