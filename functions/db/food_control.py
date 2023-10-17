from functions.config import connect_db


def get_data_food():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        sql = "SELECT id,g.id_guest,name,ifnull(confirm,0)confirm,ifnull(n_persons,0)n_persons,ifnull(amount_paid,0),ifnull(total,0)total,ifnull(ifnull(total,0)-ifnull(amount_paid,0),0)saldo,ifnull(f.status,'unpaid') status FROM guests g LEFT JOIN food f ON f.id_guest = g.id_guest WHERE id_postday= 1"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Exception as ex:
        print("[ERROR] get_data_food")
        print("[ERROR] ", ex)
        return False


def confirm_person(n_persons, id_guest):
    try:
        total = int(n_persons) * 250

        conn = connect_db()
        cursor = conn.cursor()
        sql = "UPDATE food SET n_persons = %s,total=%s WHERE id_guest = %s"
        print(sql, n_persons, total, id_guest)
        cursor.execute(sql, (n_persons, total, id_guest))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as ex:
        print("[ERROR] confirm_person")
        print("[ERROR] ", ex)
        return False


def pay_add_food(id_guest, amount_paid_in, amount_paid, total):
    try:
        if float(amount_paid_in) + float(amount_paid) - float(total) > 0:
            status = "unpaid"
        else:
            status = "paid"
        pay_amout = float(amount_paid_in) + float(amount_paid)
        conn = connect_db()
        cursor = conn.cursor()
        sql = "UPDATE food SET amount_paid =  %s,status=%s WHERE id_guest = %s"
        print(sql, amount_paid, id_guest)
        cursor.execute(sql, (pay_amout, status, id_guest))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as ex:
        print("[ERROR] pay_add_food")
        print("[ERROR] ", ex)
        return False
