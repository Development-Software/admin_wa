from functions.config import connect_db


def validate_password(username, password):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT AES_DECRYPT(password,'invites_secret') FROM users WHERE username = %s",
            (username,),
        )
        result = cursor.fetchone()
        if result is not None:
            if result[0].decode("utf-8") == password:
                return True
            else:
                return False
    except Exception as ex:
        print("[ERROR] validate_password")
        print("[ERROR] ", ex)
        return False


def get_name_user(username):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM users WHERE username = %s",
            (username,),
        )
        result = cursor.fetchone()
        if result is not None:
            return result[0]
        else:
            return False
    except Exception as ex:
        print("[ERROR] get_name_user")
        print("[ERROR] ", ex)
        return False
