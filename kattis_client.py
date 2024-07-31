import os
from autokattis import Kattis

def initialize_kattis_client():
    username = os.getenv("KATTIS_USERNAME")
    token = os.getenv("KATTIS_TOKEN")
    return Kattis(username, token)
