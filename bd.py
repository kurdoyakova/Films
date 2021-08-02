from getpass import getpass
# from mysql.connector import connect, Error
import info


def sql_connection():
    try:
        with connect(
            host="localhost",
            user=input("kurdoyakova"),
            password=getpass("15162342"),
            database="films",
        ) as con:
            print(con)
    except Error as e:
        print(e)
        raise e

        # self.type_genre = 'фильм'
        # self.type_genre = 'сериал'

def sql_create_tables_films(con):
    cursor = con.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS movies(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title_ru TEXT,
        title_eng TEXT,
        release_year YEAR(4),
        runtime TEXT;
        rating_kp DECIMAL(1,1)
        rating_imdb DECIMAL(1,1)
        storyline TEXT,
    """)
    con.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS genres (
        FOREIGN KEY(movie_id) REFERENCES movies(id));
        movie_id INT,
        genre TEXT;
    """)
    con.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS producers (
        FOREIGN KEY(movie_id) REFERENCES movies(id));
        movie_id INT,
        producer TEXT;
    """)
    con.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS countries (
        FOREIGN KEY(movie_id) REFERENCES movies(id));
        movie_id INT,
        country TEXT;
    """)
    con.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS actors (
        FOREIGN KEY(movie_id) REFERENCES movies(id));
        movie_id INT,
        actor TEXT;
    """)
    con.commit()
    cursor.close()


def sql_create_tables_serials(con):
    cursor = con.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS movies(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title_ru TEXT,
        title_eng TEXT,
        release_year YEAR(4),
        runtime TEXT;
        rating_kp DECIMAL(1,1)
        rating_imdb DECIMAL(1,1)
        number_of_seasons INT
        storyline TEXT,
    """)
    con.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS genres (
        FOREIGN KEY(movie_id) REFERENCES movies(id));
        movie_id INT,
        genre TEXT;
    """)
    con.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS producers (
        FOREIGN KEY(movie_id) REFERENCES movies(id));
        movie_id INT,
        producer TEXT;
    """)
    con.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS countries (
        FOREIGN KEY(movie_id) REFERENCES movies(id));
        movie_id INT,
        country TEXT;
    """)
    con.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS actors (
        FOREIGN KEY(movie_id) REFERENCES movies(id));
        movie_id INT,
        actor TEXT;
    """)
    con.commit()
    cursor.close()


def main(NAME):
    info.main(NAME)[0]
    # con = sql_connection()
    # if type_genre == 'фильм':
        # sql_create_tables_films(con)
    # else:
        # sql_create_tables_serials(con)


if __name__ == '__main__':
    NAME = 'сокровища нации'
    main(NAME)
