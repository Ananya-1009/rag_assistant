from database.db import get_connection
def add_message(chat_id,role,message):
    conn=get_connection()
    conn.execute("""Insert into messages(chat_id,role,message) values(?,?,?)""",(chat_id,role,message))
    conn.commit()
    conn.close()
def get_messages(chat_id):
    conn=get_connection()
    messages=conn.execute("""Select * from messages where chat_id=? order by id""",(chat_id,)).fetchall()
    conn.close()
    return messages