from flask import render_template
from website.website import app

@app.route('/')
def hello_world():
    return "Hello World"