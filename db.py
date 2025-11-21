from tinydb import TinyDB, Query
from tinydb.table import Document
import base64

class TGgroups:
    def __init__(self):
        self.query = Query()
        self.adminfile = TinyDB('group_chat_ids.json', indent=4)
        self.admintable = self.adminfile.table('GroupIDs')

    def simple_encrypt(self, text):
        encoded = base64.b64encode(text.encode()).decode()
        return encoded[::-1]

    def simple_decrypt(self, encoded):
        reversed_text = encoded[::-1]
        decoded = base64.b64decode(reversed_text.encode()).decode()
        return decoded

    def add_group(self, chat_id, fio):
        enc_id = self.simple_encrypt(str(chat_id))
        if not self.check_group_id(chat_id):
            self.admintable.insert({'chat_id': enc_id, "group_name": fio})
            return True
        else :
            return False
    
    def delete_admin(self, chat_id):
        enc_id = self.simple_encrypt(str(chat_id))
        if self.check_group_id(chat_id):
            self.admintable.remove(self.query.chat_id == enc_id)
            return True
        else:
            return False

    def view_groups(self):
        all_chat_ids = self.admintable.all()
        all_admins = []
        for admin in all_chat_ids:
            decode_id = self.simple_decrypt(admin['chat_id'])
            all_admins.append(
                {
                    'chat_id':decode_id,
                    'group_name': admin['group_name']
                }
            )
        return all_admins

    def check_group_id(self, chat_id):
        enc_id = self.simple_encrypt(str(chat_id))
        
        result = self.admintable.search(self.query.chat_id == enc_id)
        return len(result) > 0
    