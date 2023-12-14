from flask import Flask, session

app = Flask(__name__)

app.secret_key = b'fjfghr3u8487ezaYGHf783?48gf8d'


import controllers.index
import controllers.new_reader
import controllers.search

if __name__ == '__main__':
    app.run()
