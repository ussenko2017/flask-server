
# -*- coding: utf-8 -*-
"""
The flask application package.
"""

from flask import Flask
import myFunc
app = Flask(__name__)
app.secret_key = 'super secret string'  # Change this!
db = myFunc.createTables(myFunc.DBName)