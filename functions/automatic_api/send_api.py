import os
import json
import requests
import pyshorteners as ps
from functions.config import connect_db, token_wa


def send_invite(id_guest):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT id_guest,phone,name,url,id_postday,name_legal FROM guests WHERE id_guest='{id_guest}'"
        )
        rows = cursor.fetchall()
        conn.close()
        print("test")
        for row in rows:
            if row[1] is not None:
                url_invite = short_url(f"https://xvivonne.com/invite?id={row[0]}&WA=1")
                send = send_template(row[1], row[0], url_invite, row[5])
                if send == 200:
                    actualizar_estatus(row[0], "sent")
                    return True
                else:
                    actualizar_estatus(row[0], "error")
                    return False
    except Exception as e:
        print(e)
        return False


def send_confirmation(id_guest):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT id_guest,phone,name,id_postday FROM guests WHERE id_guest='{id_guest}' AND shipping>0"
        )
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            if row[1] is not None:
                send = send_message_confirmation(row[1], row[0], row[2], row[3])
                if send == 200:
                    actualizar_estatus(row[0], "confirmed")
                    return True
                else:
                    actualizar_estatus(row[0], "error")
                    return False

    except Exception as ex:
        print("[ERROR] send_confirmation")
        print("[ERROR] ", ex)
        return False


def send_room_message(id_guest):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT id_guest,phone,name,id_postday FROM guests WHERE id_guest='{id_guest}'"
        )
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            if row[1] is not None:
                send = send_confirmation_room(row[1])
                if send == 200:
                    return True
                else:
                    return False

    except Exception as ex:
        print("[ERROR] send_confirmation")
        print("[ERROR] ", ex)
        return False


def actualizar_estatus(id, status):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        if status != "error":
            cursor.execute(
                f"UPDATE guests SET status ='{status}',shipping=shipping+1,created_at=NOW() WHERE id_guest = '{id}'"
            )
        else:
            cursor.execute(
                f"UPDATE guests SET status ='{status}',created_at=NOW() WHERE id_guest = '{id}'"
            )
        conn.commit()
        conn.close()

    except Exception as e:
        print(e)


def obtener_mensaje(id, nombre, id_guest):
    # Indicador de mensajes
    # 0- Solo invitación
    # 1- Invitación y desayuno
    mensaje = ""
    if id == 0:
        mensaje = (
            f"_Hola {nombre}_\n"
            "🎉_¡Celebra con nosotros en una noche llena de magia y alegría en los XV años de *Ivonne*! Este "
            "evento tan especial marcará un nuevo capítulo en su vida, y nos encantaría contar con tu presencia "
            "para hacerlo aún más memorable._\n\n"
            "_Prepárate para disfrutar de una velada llena de música, baile y diversión, rodeados de amigos y "
            "familiares. Tu compañía será el regalo más valioso que podríamos recibir._🎁\n\n"
            "_Por favor, es *importante* confirmar tu asistencia antes del *14 de octubre* ‼️ para poder "
            "organizar todos los detalles de manera adecuada._\n\n"
            "_¡Esperamos verte y compartir juntos esta celebración inolvidable!_\n\n"
            "Atentamente,\n"
            "👨‍👩‍👧‍👧Fam. Martínez Lemus\n"
        )  # f"https://xvivonne.com/invitacion/index.php?id={id_guest}&WA=1"
    elif id == 1:
        mensaje = (
            f"_Hola {nombre}_\n"
            "🎉_¡Celebra con nosotros en una noche llena de magia y alegría en los XV años de *Ivonne*! Este "
            "evento tan especial marcará un nuevo capítulo en su vida, y nos encantaría contar con tu presencia "
            "para hacerlo aún más memorable._\n\n"
            "_Prepárate para disfrutar de una velada llena de música, baile y diversión, rodeados de amigos y "
            "familiares. Tu compañía será el regalo más valioso que podríamos recibir._🎁\n\n"
            "_Además te consideramos un invitado especial y queremos compartir contigo un delicioso desayuno🌮, "
            "organizado por el banquete, "
            "al día siguiente a las 11:00 am⏰ para prolongar la alegría de la celebración y seguir "
            "compartiendo momentos y recuerdos._\n\n"
            "_Para contribuir a los gastos de este desayuno especial, se ha establecido un costo de *$250* pesos "
            "por persona. Sabemos que cada uno de ustedes es parte importante de esta celebración, "
            "y agradecemos su consideración en este aspecto._\n\n"
            "_Por favor, es *importante* confirmar tu asistencia antes del *14 de octubre* ‼️ para poder "
            "organizar todos los detalles de manera adecuada y también pedimos de tu apoyo para que en la "
            "sección de comentarios, al momento de confirmar, nos compartas si podemos contar contigo para el "
            "desayuno._\n\n"
            "_¡Esperamos verte y compartir juntos esta celebración inolvidable!_\n\n"
            "Atentamente,\n"
            "👨‍👩‍👧‍👧Fam. Martínez Lemus\n"
        )  # f"https://xvivonne.com/invitacion/index.php?id={id_guest}&WA=1"
    return mensaje


def send_message(phone, message):
    try:
        token = os.environ.get("TOKEN_WA")
        url = f"https://graph.facebook.com/v17.0/{os.getenv('ID_WA')}/messages"
        payload = json.dumps(
            {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": f"{phone}",
                "type": "text",
                "text": {"preview_url": False, "body": f"{message}"},
            }
        )
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.status_code
    except Exception as ex:
        print("[ERROR] send_message")
        print("[ERROR] ", ex)
        return 400


def send_image(phone, url_image):
    token = token_wa()
    url = f"https://graph.facebook.com/v17.0/{os.getenv('ID_WA')}/messages"
    payload = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": f"{phone}",
            "type": "image",
            "image": {"link": f"{url_image}"},
        }
    )
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.status_code


def send_template(phone, id_guest, url_invite, name):
    try:
        invite = url_invite.split("/")[-1]
        token = token_wa()
        os.environ["ID_WA"] = "103190916217360"
        url = f"https://graph.facebook.com/v17.0/{os.getenv('ID_WA')}/messages"
        payload = json.dumps(
            {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": f"{phone}",
                "type": "template",
                "template": {
                    "name": "invitacion_para_eventos",
                    "language": {"code": "es_MX"},
                    "components": [
                        {
                            "type": "header",
                            "parameters": [
                                {
                                    "type": "image",
                                    "image": {
                                        "link": f"https://xvivonne.com/static/assets/img/QR/{id_guest}.jpg"
                                    },
                                }
                            ],
                        },
                        {
                            "type": "body",
                            "parameters": [{"type": "text", "text": f"{name}"}],
                        },
                        {
                            "type": "button",
                            "sub_type": "url",
                            "index": "0",
                            "parameters": [{"type": "text", "text": f"{invite}"}],
                        },
                    ],
                },
            }
        )
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code != 200:
            print("[ERROR] send_confirmation")
            print("[ERROR] ", response.text)
        return response.status_code
    except Exception as ex:
        print("[ERROR] send_template")
        print("[ERROR] ", ex)
        return 400


def send_confirmation_room(phone):
    try:
        token = token_wa()
        url = f"https://graph.facebook.com/v17.0/{os.getenv('ID_WA')}/messages"
        payload = json.dumps(
            {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": f"{phone}",
                "type": "template",
                "template": {
                    "name": "opcion_de_hospedaje",
                    "language": {"code": "es_MX"},
                },
            }
        )
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        # print(response.text)
        if response.status_code != 200:
            print("[ERROR] send_confirmation_room")
            print("[ERROR] ", response.text)
            return response.status_code
        else:
            return response.status_code
    except Exception as ex:
        print("[ERROR] send_confirmation_room")
        print("[ERROR] ", ex)
        return False


def send_message_confirmation(phone, id_guest, name, id_postday):
    try:
        token = token_wa()
        url = f"https://graph.facebook.com/v17.0/{os.getenv('ID_WA')}/messages"
        if id_postday == 0:
            payload = json.dumps(
                {
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": f"{phone}",
                    "type": "template",
                    "template": {
                        "name": "confirmar_solo",
                        "language": {"code": "es_MX"},
                        "components": [
                            {
                                "type": "body",
                                "parameters": [{"type": "text", "text": f"{name}"}],
                            },
                        ],
                    },
                }
            )
        elif id_postday == 1:
            payload = json.dumps(
                {
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": f"{phone}",
                    "type": "template",
                    "template": {
                        "name": "confirmacion_asistencia",
                        "language": {"code": "es_MX"},
                        "components": [
                            {
                                "type": "body",
                                "parameters": [{"type": "text", "text": f"{name}"}],
                            },
                        ],
                    },
                }
            )

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        # print(response.text)
        if response.status_code != 200:
            print("[ERROR] send_confirmation")
            print("[ERROR] ", response.text)
        return response.status_code
    except Exception as ex:
        print("[ERROR] send_message_confirmation")
        print("[ERROR] ", ex)
        return 400


def short_url(url):
    shorter_url = ps.Shortener().tinyurl.short(url)
    return shorter_url


def get_url_invite(id_guest):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT id_guest,phone,name,url,id_postday,name_legal FROM guests WHERE id_guest='{id_guest}'"
        )
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            if row[1] is not None:
                url_invite = short_url(
                    f"https://xvivonne.com/invite?id={row[0]}&ticket=1"
                )
                return url_invite
            else:
                return "https://xvivonne.com/"
    except Exception as ex:
        print("[ERROR] get_url_invite")
        print("[ERROR] ", ex)
        return "https://xvivonne.com/"
