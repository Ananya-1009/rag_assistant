import uuid
from database.chat_repository import get_all_chats
class ChatManager:
    def __init__(self):
        chats = get_all_chats()
        self.current_chat_id=chats[0]["id"]
    def get_chat_id(self):
        return self.current_chat_id
    def set_chat(self,chat_id):
        self.current_chat_id=chat_id
chat_manager=ChatManager()