import uuid
from database.db import get_connection
def create_chat(title="New Chat"):
    conn=get_connection()
    cursor=conn.cursor()
    chat_id=str(uuid.uuid4())
    cursor.execute(
        """Insert into chats(id,title) values(?,?)""",(chat_id,title)
    )
    conn.commit()
    conn.close()
    return chat_id
def get_all_chats():
    conn=get_connection()
    chats=conn.execute("""Select * from chats order by created_at desc""").fetchall()
    conn.close()
    return chats
def get_chat(chat_id):
    conn=get_connection()
    chat=conn.execute("""Select * from chats where  id=?""",(chat_id,)).fetchone()
    conn.close()
    return chat

