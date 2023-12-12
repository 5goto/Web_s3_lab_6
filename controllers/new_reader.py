from app import app
from flask import render_template, request, session, redirect, url_for
from utils import get_db_connection
from models.index_model import get_new_reader


@app.route('/new_reader', methods=['get'])
def new_reader():
    return render_template(
            "new_reader.html"
    )