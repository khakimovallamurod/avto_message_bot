import os
from dotenv import load_dotenv
import ast

load_dotenv()
def get_token():
    TOKEN = os.getenv("TOKEN")
    if TOKEN is None:
        raise ValueError("TOKEN not found.")
    return TOKEN

def get_adminIds():
    admin_ids = os.getenv("admin_ids")
    if admin_ids is None:
        raise ValueError("admin ids not found.")
    
    admin_list = ast.literal_eval(admin_ids)
    return admin_list
