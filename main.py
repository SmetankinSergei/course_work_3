from enum import Enum

from flask import Flask

app = Flask(__name__)
current_user = None
search_session = None
temp_user_photo = None

import routes
