from functions.config import connect_db


def get_url_invite(id_guest):
    try:
        db = connect_db()
        cursor = db.cursor()
        sql = f"SELECT url FROM guests WHERE id_guest = '{id_guest}'"
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        db.close()
        return result[0]
    except Exception as e:
        print(e)
        return "https://xvivonne.com/"


def insert_record(id_guest, type):
    try:
        if type == "wa":
            type = "WhatsApp"
        elif type == "qr":
            type = "QR"
        else:
            type = "Guest"
        db = connect_db()
        cursor = db.cursor()
        sql = f"INSERT INTO records (id_guest,type,created_at) VALUES ('{id_guest}','{type}',NOW())"
        cursor.execute(sql)
        rows_affected = cursor.rowcount
        db.commit()
        cursor.close()
        db.close()
        if rows_affected > 0:
            update_guest(id_guest, "income")
        else:
            update_guest(id_guest, "error")
    except Exception as e:
        print(e)


def update_guest(id_guest, status):
    try:
        db = connect_db()
        cursor = db.cursor()
        sql = f"UPDATE guests SET status = '{status}' WHERE id_guest = '{id_guest}' AND status not in ('confirmed','no_confirmed')"
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()
        return True
    except Exception as e:
        print(e)
        return False


def validate_confirm(id):
    try:
        db = connect_db()
        cursor = db.cursor()
        sql = f"SELECT count(*) FROM guests WHERE id_guest = '{id}' and status = 'confirmed'"
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        db.close()
        if result[0] > 0:
            return True
        else:
            return False
    except Exception as e:
        return False
