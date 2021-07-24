import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
"Accept-language":"ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"}

def print_info_film(type_genre,ru_name,eng_name,release_year,country,producer,runtime,genre,rating_kp,rating_imdb,actor,storyline):
	table = [['type', type_genre],['ru_name', ru_name], ['eng_name', eng_name], ['release_year', release_year],
		['country', country], ['producer', producer], ['runtime', runtime],
		['genres', genre], ['rating_kp', rating_kp], ['rating_imdb', rating_imdb],['actors', actor], ['storyline', storyline]]
	print(tabulate(table, tablefmt="plain"))

def print_info_serail(type_genre,number_of_seasons,ru_name,eng_name,release_year,country,producer,runtime,genre,rating_kp,rating_imdb,actor,storyline):
	table = [['type', type_genre],['number of seasons', number_of_seasons],['ru_name', ru_name], ['eng_name', eng_name], ['release_year', release_year],
		['country', country], ['producer', producer], ['runtime', runtime],
		['genres', genre], ['rating_kp', rating_kp], ['rating_imdb', rating_imdb],['actors', actor], ['storyline', storyline]]
	print(tabulate(table, tablefmt="plain"))

def kp_type(url):	
	response = requests.get(url, headers = headers)
	if response.status_code == 200:
		print("-- kinopoisk works --")
	elif response.status_code == 404:
		print('-- not found --')
	else:
		print("-- something is wrong --",response.status_code)
	soup = BeautifulSoup(response.content, "html.parser")

	quotes_for_type = soup.find_all('div', class_='styles_title__1yvs9')
	if quotes_for_type == []:
		quotes_for_type = soup.find_all('div', class_='styles_title__3tVSa')
		type_with_year = quotes_for_type[0].contents[0].contents[2].text
		type_genre = type_with_year[1:7]
	else:
		type_genre = 'фильм'
	return type_genre,soup

def kp_info_film(url,soup):
	quotes = soup.find_all('div', class_="styles_rowDark__2qC4I styles_row__2ee6F")
	quotes2 = soup.find_all('div', class_='styles_title__1yvs9')
	quotes3 = soup.find_all('div', class_='styles_body__2Ynqg')
	quotes4 = soup.find_all('div', class_='styles_filmSynopsis__zLClu')
	quotes5 = soup.find_all('div', class_="styles_actors__2zt1j")

	release_year = (quotes[0].contents)[1].text
	ru_name_with_year = (quotes2[0].contents)[0].contents[0].text
	ru_name = ru_name_with_year[:len(ru_name_with_year)-6]
	eng_name = (quotes2[0].contents)[1].contents[0].text
	country = (quotes[1].contents)[1].text
	rating_kp = (quotes3[0].contents)[0].text

	runtime_full = (quotes[len(quotes)-1].contents)[1].text
	for i in runtime_full:
		if i == '/':
			runtime = runtime_full[len(runtime_full)-6:len(runtime_full)]
			break
		else:
			runtime = runtime_full[0:len(runtime_full)-1]

	genre = []
	genres = (quotes[2].contents)[1].contents[0].contents
	for i in range(0,len(genres),2):
		genre.append(genres[i].text)

	producer = []
	producers = (quotes[4].contents)[1].contents
	for i in range(0,len(producers),2):
		if producers[i].text == '...':
			break
		producer.append(producers[i].text)

	if quotes4 == []:
		storyline = '-'
	else:
		storyline = quotes4[0].text

	actor = []
	actors = (quotes5[0].contents)[1].contents
	for i in range(0,len(actors)):
		actor.append(actors[i].text)

	return ru_name,eng_name,release_year,country,producer,runtime,genre,rating_kp,actor,storyline

def kp_info_serial(url,soup):
	quotes = soup.find_all('div', class_='styles_rowLight__3uy9z styles_row__2ee6F')
	quotes2 = soup.find_all('div', class_='styles_title__3tVSa')
	quotes3 = soup.find_all('div', class_='styles_body__2Ynqg')
	quotes4 = soup.find_all('div', class_='styles_filmSynopsis__zLClu')
	quotes5 = soup.find_all('div', class_="styles_actors__2zt1j")

	release_year_with_number_of_seasons = (quotes[0].contents)[1].text
	release_year = release_year_with_number_of_seasons[0:4]
	number_of_seasons = release_year_with_number_of_seasons[6:7]
	ru_name = (quotes2[0].contents)[0].contents[0].text
	eng_name = (quotes2[0].contents)[1].contents[0].text
	country = (quotes[1].contents)[1].text
	rating_kp = (quotes3[0].contents)[0].text

	runtime_full = (quotes[len(quotes)-1].contents)[1].text
	for i in runtime_full:
		if i == '/':
			runtime = runtime_full[len(runtime_full)-6:len(runtime_full)]
			break
		else:
			runtime = runtime_full[0:len(runtime_full)-1]

	genre = []
	genres = (quotes[2].contents)[1].contents[0].contents
	for i in range(0,len(genres),2):
		genre.append(genres[i].text)

	producer = []
	producers = (quotes[4].contents)[1].contents
	for i in range(0,len(producers),2):
		if producers[i].text == '...':
			break
		producer.append(producers[i].text)

	if quotes4 == []:
		storyline = '-'
	else:
		storyline = quotes4[0].text

	actor = []
	actors = (quotes5[0].contents)[1].contents
	for i in range(0,len(actors)):
		actor.append(actors[i].text)

	return number_of_seasons,ru_name,eng_name,release_year,country,producer,runtime,genre,rating_kp,actor,storyline

def imdb_info(url):
	response = requests.get(url, headers = headers)
	if response.status_code == 200:
		print("-- IMDb works --")
	else:
		print("-- something is wrong --",response.status_code)
	soup = BeautifulSoup(response.content, "html.parser")

	quotes_for_rating_imdb = soup.find_all('div', class_="AggregateRatingButton__ContentWrap-sc-1ll29m0-0 hmJkIS")
	rating_imdb = (quotes_for_rating_imdb[0].contents)[0].contents[0].text
	return rating_imdb

def find_url_kp(name):
	words = name.split()
	name_like_url = words[0]
	for i in range(1,len(words)):
		name_like_url = str(name_like_url) + '+' + str(words[i])
	url = 'https://www.kinopoisk.ru/index.php?kp_query=' + str(name_like_url)

	response = requests.get(url, headers = headers)
	if response.status_code == 200:
		print("-- kinopoisk works --")
	elif response.status_code == 404:
		print('-- not found --')
	else:
		print("-- something is wrong --",response.status_code)
	soup = BeautifulSoup(response.content, "html.parser")

	quotes_for_id_kp = soup.find_all('p', class_='name')
	id_kp = quotes_for_id_kp[0].contents[0].get('data-url')
	url_kp =  'https://www.kinopoisk.ru' + str(id_kp)
	return url_kp

def find_url_imdb(name):
	words = name.split()
	name_like_url = words[0]
	for i in range(1,len(words)):
		name_like_url = str(name_like_url) + '+' + str(words[i])
	url = 'https://www.imdb.com/find?q=' + str(name_like_url) + '&ref_=nv_sr_sm'

	response = requests.get(url, headers = headers)
	if response.status_code == 200:
		print("-- IMDb works --")
	elif response.status_code == 404:
		print('-- not found --')
	else:
		print("-- something is wrong --",response.status_code)
	soup = BeautifulSoup(response.content, "html.parser")

	quotes_for_id_imdb = soup.find_all('table', class_='findList')
	quotes_cool = quotes_for_id_imdb[0].contents[1].contents[1].contents[1]
	id_imdb = quotes_cool.get('href')
	url_imdb =  'https://www.imdb.com' + str(id_imdb)
	return url_imdb

def main(name):
	url_kp = find_url_kp(name)
	type_genre,soup = kp_type(url_kp)

	if type_genre == 'фильм':
		ru_name,eng_name,release_year,country,producer,runtime,genre,rating_kp,actor,storyline = kp_info_film(url_kp,soup)
		url_imdb = find_url_imdb(eng_name)
		rating_imdb = imdb_info(url_imdb)
		print_info_film(type_genre,ru_name,eng_name,release_year,country,producer,runtime,genre,rating_kp,rating_imdb,actor,storyline)
	else:
		number_of_seasons,ru_name,eng_name,release_year,country,producer,runtime,genre,rating_kp,actor,storyline = kp_info_serial(url_kp,soup)
		url_imdb = find_url_imdb(eng_name)
		rating_imdb = imdb_info(url_imdb)
		print_info_serail(type_genre,number_of_seasons,ru_name,eng_name,release_year,country,producer,runtime,genre,rating_kp,rating_imdb,actor,storyline)

if __name__ == '__main__':
	name = 'грань'
	main(name)