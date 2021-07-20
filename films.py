from getpass import getpass
from mysql.connector import connect, Error


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

def sql_create_tables(con):
	cursor = con.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS movies(
    	id INTEGER PRIMARY KEY AUTOINCREMENT,
    	title TEXT,
    	release_year YEAR(4),
    	genre TEXT;
    	country TEXT;
    	producer TEXT;
    	runtime TEXT;
	""")
    con.commit()

	cursor.execute("""CREATE TABLE IF NOT EXISTS ratings (
		movie_id INT,
    	name_of_site TEXT,
    	rating INT
    	FOREIGN KEY(movie_id) REFERENCES movies(id));
	""")
	con.commit()

	cursor.execute("""CREATE TABLE IF NOT EXISTS storyline (
		movie_id INT,
    	storyline TEXT,
    	FOREIGN KEY(movie_id) REFERENCES movies(id));
	""")
	con.commit()
	cursor.close()


def main():
    con = sql_connection()
    sql_create_tables(con)





if __name__ == '__main__':
    main()
