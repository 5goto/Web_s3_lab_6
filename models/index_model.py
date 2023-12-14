import pandas
from datetime import datetime


def get_reader(conn):
    return pandas.read_sql(
        '''
 SELECT * FROM reader
 ''', conn)


def get_book_reader(conn, reader_id):
    # выбираем и выводим записи о том, какие книги брал читатель
    return pandas.read_sql('''
 WITH get_authors( book_id, authors_name)
 AS(
 SELECT book_id, GROUP_CONCAT(author_name)
 FROM author JOIN book_author USING(author_id)
 GROUP BY book_id
 )
 SELECT title AS Название, authors_name AS Авторы,
 borrow_date AS Дата_выдачи, return_date AS Дата_возврата,
 book_reader_id
 FROM
 reader
 JOIN book_reader USING(reader_id)
 JOIN book USING(book_id)
 JOIN get_authors USING(book_id)
 WHERE reader.reader_id = :id
 ORDER BY 3
 ''', conn, params={"id": reader_id})


# для обработки данных о новом читателе
def get_new_reader(conn, new_reader):
    cur = conn.cursor()
    cur.execute("insert into reader (reader_name) values (:name)", {"name": new_reader})
    conn.commit()
    return cur.lastrowid


# сдаем книгу
def return_book(conn, book_reader_id, reader_id):
    current_date = datetime.now().strftime('%Y-%m-%d')
    cur = conn.cursor()
    try:
        cur.execute('BEGIN')
        book_id = cur.execute(f'''SELECT book_id FROM book_reader WHERE book_reader_id = {book_reader_id}''').fetchone()[0]
        if book_id is None:
            return

        cur.execute(f'''update book_reader 
        set return_date = '{current_date}' 
        where reader_id = {reader_id} 
        and book_reader_id = {book_reader_id}''')

        cur.execute(f'''UPDATE book
        SET available_numbers = available_numbers + 1
        WHERE book_id = {book_id}''')

        conn.commit()
    except Exception as e:
        conn.rollback()
        print('Ошибка при выполнении транзакции: ', e)


# для обработки данных о взятой книге
def borrow_book(conn, book_id, reader_id):
    cur = conn.cursor()
    # добавить взятую книгу (book_id) читателю (reader_id) в таблицу book_reader
    # указать текущую дату как дату выдачи книги
    # уменьшить количество экземпляров взятой книги
    return True
