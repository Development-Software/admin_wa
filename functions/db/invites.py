from functions.config import connect_db


def get_data_invites():
    db = connect_db()
    cursor = db.cursor()
    sql = (
        "SELECT g.id_guest,name,phone,status,g.created_at "
        "FROM guests g "        
        "ORDER BY g.name"
    )
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result
