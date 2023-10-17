import os
import logging
import qrcode
from PIL import Image
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import CircleModuleDrawer, SquareModuleDrawer
from functions.config import connect_db


def get_data_guest():
    db = connect_db()
    cursor = db.cursor()
    sql = (
        "SELECT g.id_guest,name,phone,adults,teenagers,kids,(adults+teenagers+kids)total,url,id_postday,id_room,name_legal "
        "FROM guests g "
        "INNER JOIN guest_person gp ON g.id_guest = gp.id_guest"
    )
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result


def get_number_guest():
    options = [{"value": str(i), "text": str(i)} for i in range(0, 10)]
    return options


def action_guest(
    action, id, name, phone, adults, tennagers, kids, url, id_invite, food, room, legal
):
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(
            "CREATE TEMPORARY TABLE OutputTable (response INT,uid VARCHAR(36));"
        )
        print(
            action,
            id,
            name,
            phone,
            adults,
            tennagers,
            kids,
            url,
            id_invite,
            food,
            room,
            legal,
        )
        cursor.execute(
            f"CALL action_guest('{action}', '{id}', '{name}', '{phone}', {adults}, {tennagers},{kids}, '{url}', '{id_invite}', {food}, {room},'{legal}', @result,@uid_out);"
        )
        cursor.execute(
            "INSERT INTO OutputTable (response,uid) VALUES (@result,@uid_out);"
        )
        cursor.execute("SELECT response,uid FROM OutputTable;")
        # cursor.execute("DROP TABLE OutputTable;")
        result = cursor.fetchall()
        db.commit()
        cursor.close()
        db.close()
        if result is not None:
            if result[0][0] == 1:
                if action == "add_guest":
                    print("created_qr")
                    created_qr(result[0][1])
                return True
        else:
            return False
    except Exception as e:
        print("action_guest error")
        print(e)
        return False


def created_qr(id):
    try:
        # Llenamos de datos el código QR
        url = f"https://xvivonne.com/invite?id={id}&QR=1"  # URL del Código
        qr = qrcode.QRCode(
            version=10,
            # https://github.com/lincolnloop/python-qrcode/blob/df139670ac44382d4b70820edbe0a9bfda9072aa/qrcode/util.py#L183
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            # border=18,
            mask_pattern=4,  # https://www.thonky.com/qr-code-tutorial/mask-patterns,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # Agregamos nuestra imagen al código QR
        QRimg = qr.make_image(
            fill_color="white",
            back_color=None,
            image_factory=StyledPilImage,
            module_drawer=CircleModuleDrawer(resample_method=None),
            eye_drawer=SquareModuleDrawer(),
        )
        # Guardamos la imagen de nuestro código QR en un directorio
        QRimg.save(f"functions/create_qr/QRs/preview/{id}.jpg")

        # Abrir las imágenes
        imagen_grande = Image.open(f"functions/create_qr/QRs/preview/{id}.jpg")
        imagen_pq = Image.open("functions/create_qr/QRs/XV.png")

        # Redimensionar la imagen pequeña al tamaño deseado
        new_size = (250, 250)  # Cambia este tamaño a tus preferencias
        imagen_pq_rz = imagen_pq.resize(new_size)

        # Superponer la imagen pequeña redimensionada sobre la imagen grande
        pos = (200, 200)  # Cambia esta posición a tus preferencias
        imagen_grande.paste(imagen_pq_rz, pos, imagen_pq_rz)

        # Mostrar la imagen resultante
        # imagen_grande.show()
        imagen_grande.save(f"static/assets/img/QR/{id}.jpg")
        os.remove(f"functions/create_qr/QRs/preview/{id}.jpg")
        print("created_qr success")
        print(id)
        return True
    except Exception as e:
        print("created_qr error")
        print(e)
        return False
