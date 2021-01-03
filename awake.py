from flask import Flask
from threading import Thread

app = Flask('')

# creating the route
# printing "Still Awake" when online
@app.route('/')
def home():
    return "Still Awake"

# pinging the url so it doesnt expire
def run():
  app.run(host='0.0.0.0',port=8080)

# it runs constantly
def insomnia():
    t = Thread(target=run)
    t.start()