from functions.config import connect_db


def get_data_invites():
    db = connect_db()
    cursor = db.cursor()
    sql = (
        "SELECT g.id_guest,name,phone,(adults+teenagers+kids)total,status,shipping,CASE WHEN views IS NULL THEN 0 ELSE views END views,id_postday,id_room,g.created_at "
        "FROM guests g "
        "INNER JOIN guest_person gp ON g.id_guest = gp.id_guest "
        "LEFT JOIN (SELECT id_guest,count(id_guest) views FROM records group by id_guest ) r ON g.id_guest = r.id_guest "
        "ORDER BY g.name"
    )
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result
