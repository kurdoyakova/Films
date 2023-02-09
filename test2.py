import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from numpy import empty
from getpass import getpass
from mysql.connector import connect, Error
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

type_genre = 'фильм'
ru_name = 'Начало'
eng_name = 'Inception'
release_year = 1998
country = ['США', 'Мексика']
producer = ['Джон Хьюстон']
runtime = '02:06'
genre = ['драма', 'приключения', 'вестерн', 'боевик']
rating_kp = 8.0
rating_imdb = 8.2
actor = ['Хамфри Богарт', 'Уолтер Хьюстон', 'Тим Холт', 'Брюс Беннетт', 'Бартон МакЛэйн', 'Альфонсо Бедойа', 'Артуро Сото Рангель', 'Мануэль Донде', 'Хосе Тровей', 'Маргарито Луна']
storyline = 'В небольшом мексиканском городке Тампико знакомятся два бедняка Доббс и Кертин. От местного старика они узнают о золотой жиле в окрестностях Сьерра Мадре. Вложив все свои деньги в дело, трое друзей отправляются в опасное путешествие.Дойти туда стоит огромных трудов, но сохранить трезвый разум при виде жёлтого металла и вернуться живым ещё сложнее.'


def test2(**kwargs):
	table = []
	for k, v in kwargs.items():
	    table.append([str(k),v])
	print(tabulate(table, tablefmt="plain"))


# test2(type=type_genre, ru_name=ru_name, eng_name=eng_name,
# 	release_year=release_year, country=country, producer=producer,
# 	runtime=runtime, genre=genre, rating_kp=rating_kp, rating_imdb=rating_imdb,
# 	actor=actor, storyline=storyline)

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

# info.main(NAME)
con = sql_connection()
sql_create_tables_films(con)
