from enum import Enum

from flask import Flask

app = Flask(__name__)
current_user = None
search_users_from_id = 1
import routes
