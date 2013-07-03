from flask import render_template as render

from bodha import app


@app.route('/')
def index():
    return render('index.html')
