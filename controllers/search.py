from app import app
from flask import render_template, request, session
from utils import get_db_connection, join_string
from models.search_model import get_books, get_counted_publishers, get_counted_authors, get_counted_genres, take_book


@app.route('/search', methods=['get'])
def search():
    search_genres = request.values.getlist('Жанр')
    search_authors = request.values.getlist('Автор')
    search_publishers = request.values.getlist('Издательство')

    taken_book_id = request.values.get('take_book_id')
    user_id = session['reader_id']

    conn = get_db_connection()

    if taken_book_id:
        take_book(conn, taken_book_id, user_id)

    books = get_books(conn, search_genres, search_authors, search_publishers)

    counted_authors = get_counted_authors(conn).to_dict(orient='records')
    counted_genres = get_counted_genres(conn).to_dict(orient='records')
    counted_publishers = get_counted_publishers(conn).to_dict(orient='records')

    return render_template(
        "search.html",
        table_name=['Книги'],
        relations=[books],
        authors=counted_authors,
        genres=counted_genres,
        publishers=counted_publishers,
        search_genres=search_genres,
        search_authors=search_authors,
        search_publishers=search_publishers,
        join_string=join_string,
        len=len,
        zip=zip,
        list=list,
    )
