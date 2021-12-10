# this file interacts with the Flask app to call our bot once every 10 minutes to ensure that our bot does not go to sleep and can always be interacted with
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Hello. I am alive!"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()