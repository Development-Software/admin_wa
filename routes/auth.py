# auth.py
import os

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,
)
from functions.db.dashboard import get_data_guest, get_number_guest, action_guest
from functions.db.invites import get_data_invites
from functions.automatic_api.send_api import (
    send_invite,
    send_confirmation,
    send_room_message,
)
from functions.db.invite import insert_record, get_url_invite, validate_confirm
from functions.db.login import validate_password, get_name_user
from functions.db.food_control import get_data_food, confirm_person, pay_add_food

auth_bp = Blueprint("auth", __name__)

users = {"user1": "password1", "user2": "password2"}


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if validate_password(username, password):
            session["username"] = username
            session["name"] = get_name_user(username)
            return jsonify(success=True)
        return jsonify(success=False, message="Las credenciales son invalidas")
    elif request.method == "GET":
        if "username" in session:
            return redirect(url_for("auth.dashboard"))
    return render_template("html/login.html")


@auth_bp.route("/dashboard")
def dashboard():
    if "username" in session:
        # username = session['username']
        datos = get_data_guest()
        return render_template(
            "html/dashboard.html",
            datos=datos,
            options=get_number_guest(),
            name=session["name"],
        )
    return render_template("html/login.html")


@auth_bp.route("/invites")
def invites():
    if "username" in session:
        # username = session['username']
        datos = get_data_invites()
        return render_template("html/invites.html", datos=datos, name=session["name"])
    return render_template("html/login.html")


@auth_bp.route("/food_control")
def food_control():
    if "username" in session:
        # username = session['username']
        datos = get_data_food()
        return render_template(
            "html/food_control.html",
            datos=datos,
            name=session["name"],
            options=get_number_guest(),
        )
    return render_template("html/login.html")


@auth_bp.route("/send_invitation", methods=["POST"])
def send_invitation():
    id_guest = request.form.get("id")
    # id = request.data.decode("utf-8")
    print(id_guest)
    sent = send_invite(id_guest)
    if sent:
        return jsonify(success=True, message="Invitación enviada correctamente")
    else:
        return jsonify(success=False, message="Error al enviar la invitación")


@auth_bp.route("/send_confirm", methods=["POST"])
def send_confirm():
    id_guest = request.form.get("id")
    sent = send_confirmation(id_guest)
    if sent:
        return jsonify(success=True, message="Confirmación enviada correctamente")
    else:
        return jsonify(success=False, message="Error al enviar la confirmación")


@auth_bp.route("/send_bulk_invite", methods=["POST"])
def send_bulk_invites():
    count_ok = 0
    count_error = 0
    selected_data = request.json
    for item in selected_data:
        id_value = item["id"]
        sent = send_invite(id_value)
        if sent:
            count_ok += 1
        else:
            count_error += 1
    if count_error > 0:
        return jsonify(
            success=False,
            message=f"Invitaciones enviadas correctamente: {count_ok} / Errores: {count_error}",
        )
    else:
        return jsonify(
            success=True,
            message=f"Invitaciones enviadas correctamente: {count_ok} / Errores: {count_error}",
        )


@auth_bp.route("/send_bulk_confirm", methods=["POST"])
def send_bulk_confirm():
    count_ok = 0
    count_error = 0
    selected_data = request.json
    for item in selected_data:
        id_value = item["id"]
        sent = send_confirmation(id_value)
        if sent:
            count_ok += 1
        else:
            count_error += 1
    if count_error > 0:
        return jsonify(
            success=False,
            message=f"Confirmaciones enviadas correctamente: {count_ok} / Errores: {count_error}",
        )
    else:
        return jsonify(
            success=True,
            message=f"Confirmaciones enviadas correctamente: {count_ok} / Errores: {count_error}",
        )


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    # return render_template("html/login.html")
    return redirect(url_for("auth.login"))


@auth_bp.route("/form_guest", methods=["POST"])
def add_guest():
    if request.method == "POST":
        action = request.form.get("action")
        id_guest = request.form.get("modalEditUserID")
        name = request.form.get("modalEditUserName")
        phone = request.form.get("modalEditUserPhone")
        adults = request.form.get("modalEditAdultGuests")
        teenagers = request.form.get("modalEditTeenGuests")
        kids = request.form.get("modalEditKidGuests")
        url = request.form.get("modalEditUserURL")
        legal = request.form.get("modalEditUserlegal")
        print(legal)
        food = request.form.get("food")
        room = request.form.get("room")
        part = url.split("/")
        id_invite = part[-1]
        result = action_guest(
            action,
            id_guest,
            name,
            phone,
            adults,
            teenagers,
            kids,
            url,
            id_invite,
            food,
            room,
            legal,
        )
        return jsonify(success=True, message="Datos guardados correctamente")
    return jsonify(error=True, message="Error al guardar los datos")


@auth_bp.route("/invite", methods=["GET"])
def invite():
    args = request.args
    lowercase_args = {key.lower(): value for key, value in args.items()}
    confirmed = validate_confirm(lowercase_args["id"])
    if "ticket" in lowercase_args:
        if "id" not in lowercase_args:
            return redirect("https://xvivonne.com/")
        else:
            if "wa" in lowercase_args:
                insert_record(lowercase_args["id"], "wa")
            elif "qr" in lowercase_args:
                insert_record(lowercase_args["id"], "qr")
            else:
                insert_record(lowercase_args["id"], "guest")
            url_invite = get_url_invite(lowercase_args["id"])
            return redirect(url_invite)
    else:
        return redirect(url_for("post_confirm", id=lowercase_args["id"]))


@auth_bp.route("/confirm_food", methods=["POST"])
def confirm_food():
    if request.method == "POST":
        id_guest = request.form.get("modalEditUserID")
        adults = request.form.get("modalEditAdultGuests")
        result = confirm_person(adults, id_guest)
        if result:
            return jsonify(success=True, message="Datos guardados correctamente")
        else:
            return jsonify(error=True, message="Error al guardar los datos")


@auth_bp.route("/pay_food", methods=["POST"])
def pay_food():
    if request.method == "POST":
        id_guest = request.form.get("modalpayUserID")
        amount_paid = request.form.get("modalamountUserName")
        total = request.form.get("modaltotal")
        paid_amount = request.form.get("modalpay")
        result = pay_add_food(id_guest, amount_paid, paid_amount, total)
        if result:
            return jsonify(success=True, message="Datos guardados correctamente")
        else:
            return jsonify(error=True, message="Error al guardar los datos")


@auth_bp.route("/send_room", methods=["POST"])
def send_room():
    if request.method == "POST":
        id_guest = request.form.get("id_guest")
        result = send_room_message(id_guest)
        if result:
            return jsonify(success=True, message="Datos enviados correctamente")
        else:
            return jsonify(error=True, message="Error al enviar los datos")
