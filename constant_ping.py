from flask import *
from threading import Thread
from datetime import *
import discord

app = Flask(__name__)

@app.route('/')
def home():
  return render_template('index.html',_time = datetime.now())

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():  
    t = Thread(target=run)
    t.start()