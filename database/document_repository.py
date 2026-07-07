from database.db import get_connection
def add_document(chat_id,document_id,filename):
    conn=get_connection()
    conn.execute("""Insert into documents(chat_id,document_id,filename) values(?,?,?)""",(chat_id,document_id,filename))
    conn.commit()
    conn.close()
def get_documents(chat_id):
    conn=get_connection()
    documents=conn.execute("""Select * from documents where chat_id=? order by id desc""",(chat_id,)).fetchall()
    conn.close()
    return documents
def delete_documents(chat_id):
    conn = get_connection()
    conn.execute(
        "DELETE FROM documents WHERE chat_id=?",
        (chat_id,)
    )
    conn.commit()
    conn.close()