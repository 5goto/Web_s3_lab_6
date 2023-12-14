from datetime import datetime

import pandas


def get_books(conn, genres, authors, publishers):
    query = ''

    # Добавляем условие для жанров, если список не пуст
    if genres:
        genres_str = ', '.join(['"{}"'.format(genre) for genre in genres])
        query += ' WHERE Жанр IN ({})'.format(genres_str)

    # Добавляем условие для авторов, если список не пуст и уже есть условие для жанров
    if authors and genres:
        authors_str = ', '.join(['"{}"'.format(author) for author in authors])
        query += ' AND Автор IN ({})'.format(authors_str)
    elif authors:  # Если список жанров пуст, добавляем условие для авторов независимо
        authors_str = ', '.join(['"{}"'.format(author) for author in authors])
        query += ' WHERE Автор IN ({})'.format(authors_str)

    # Добавляем условие для издательств, если список не пуст и уже есть условия для жанров и авторов
    if publishers and genres and authors:
        publishers_str = ', '.join(['"{}"'.format(publisher) for publisher in publishers])
        query += ' AND Издатель IN ({})'.format(publishers_str)
    elif publishers and (
            genres or authors):  # Если список жанров или авторов пуст, добавляем условие для издательств независимо
        publishers_str = ', '.join(['"{}"'.format(publisher) for publisher in publishers])
        query += ' WHERE Издатель IN ({})'.format(publishers_str)

    return pandas.read_sql(
        f'''WITH concat_authors AS
        (SELECT DISTINCT book_id, title AS Название_книги, genre_name as Жанр, publisher_name as Издатель,
                GROUP_CONCAT(author_name, ', ') as author_name, author_name as Автор, year_publication as Год_издания,
                available_numbers as Количество
        FROM book
        natural JOIN book_author
        natural JOIN author
        natural JOIN genre
        natural JOIN publisher
        GROUP BY title)
        select DISTINCT title as Название, concat_authors.author_name as Авторы, Жанр, Издатель, Год_издания,
               Количество, book_id
            from book_reader
            natural join reader
            natural join book
            natural join concat_authors
            {query};''', conn
    )


def take_book(conn, book_id, reader_id):
    current_date = datetime.now().strftime('%Y-%m-%d')
    cur = conn.cursor()
    try:
        cur.execute('BEGIN')
        # по хорошему надо проверять что книга есть в библиотеке
        # но в академических целях можно и не проверять
        cur.execute(f'''
            INSERT INTO book_reader(book_id, reader_id, borrow_date, return_date)
              VALUES
              ( {book_id}, {reader_id}, {current_date}, NULL)
        ''')

        cur.execute(f'''UPDATE book
                SET available_numbers = available_numbers - 1
                WHERE book_id = {book_id}''')

        conn.commit()
    except Exception as e:
        conn.rollback()
        print('Ошибка при выполнении транзакции: ', e)


def get_counted_authors(conn):
    return pandas.read_sql('''
        select author_name as Автор, count(author_name) from book
        natural join book_author
        natural join author
        group by Автор;
    ''', conn)


def get_counted_genres(conn):
    return pandas.read_sql('''
        select genre_name as Жанр, count(genre_name) from book
        natural join genre
        group by Жанр;
        ''', conn)


def get_counted_publishers(conn):
    return pandas.read_sql('''
        select publisher_name as Издательство, count(publisher_name) from book
        natural join publisher
        group by Издательство;
        ''', conn)
