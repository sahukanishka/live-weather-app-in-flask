from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('template.html')



if __name__=='__main__':
    app.debug=True
    app.run(host='0.0.0.0',port=3000) 