import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
"Accept-language":"ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"}

def print_info(ru_name,eng_name,release_year,country,producer,runtime,genre,rating_kp,rating_imdb,actor,storyline):
	table = [['ru_name', ru_name], ['eng_name', eng_name], ['release_year', release_year],
		['country', country], ['producer', producer], ['runtime', runtime],
		['genres', genre], ['rating_kp', rating_kp], ['rating_imdb', rating_imdb],['actors', actor], ['storyline', storyline]]
	print(tabulate(table, tablefmt="plain"))

def kp_info(url):	
	response = requests.get(url, headers = headers)
	if response.status_code == 200:
		print("-- everything is ok with the request for kinopoisk --")
	elif response.status_code == 404:
		print('-- not found --')
	else:
		print("-- something is wrong --",response.status_code)
	
	soup = BeautifulSoup(response.content, "html.parser")

	quotes = soup.find_all('div', class_='styles_rowLight__3uy9z styles_row__2ee6F')
	if quotes == []:
		quotes = soup.find_all('div', class_="styles_rowDark__2qC4I styles_row__2ee6F")
	release_year = (quotes[0].contents)[1].text

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

	producer = (quotes[4].contents)[1].text
	country = (quotes[1].contents)[1].text
	
	quotes2 = soup.find_all('div', class_='styles_title__1yvs9')
	ru_name_with_year = (quotes2[0].contents)[0].text
	ru_name = ru_name_with_year[:len(ru_name_with_year)-6]
	eng_name = (quotes2[0].contents)[1].contents[0].text

	quotes3 = soup.find_all('div', class_='styles_body__2Ynqg')
	rating_kp = (quotes3[0].contents)[0].text

	quotes4 = soup.find_all('div', class_='styles_filmSynopsis__zLClu')
	if quotes4 == []:
		storyline = '-'
	else:
		storyline = quotes4[0].text

	quotes5 = soup.find_all('div', class_="styles_actors__2zt1j")
	actor = []
	actors = (quotes5[0].contents)[1].contents
	for i in range(0,len(actors)):
		actor.append(actors[i].text)

	return ru_name,eng_name,release_year,country,producer,runtime,genre,rating_kp,actor,storyline

def imdb_info(url):
	response = requests.get(url, headers = headers)
	if response.status_code == 200:
		print("-- everything is ok with the request for IMDb --")
	else:
		print("-- something is wrong --",response.status_code)
	
	soup = BeautifulSoup(response.content, "html.parser")

	quotes = soup.find_all('div', class_="AggregateRatingButton__ContentWrap-sc-1ll29m0-0 hmJkIS")
	rating_imdb = (quotes[0].contents)[0].contents[0].text
	return rating_imdb

def find_url_kp(name):
	words = name.split()
	name_like_url = words[0]
	for i in range(1,len(words)):
		name_like_url = str(name_like_url) + '+' + str(words[i])
	url = 'https://www.kinopoisk.ru/index.php?kp_query=' + str(name_like_url)

	response = requests.get(url, headers = headers)
	if response.status_code == 200:
		print("-- everything is ok with the request for kinopoisk --")
	elif response.status_code == 404:
		print('-- not found --')
	else:
		print("-- something is wrong --",response.status_code)
	
	soup = BeautifulSoup(response.content, "html.parser")

	quotes = soup.find_all('p', class_='name')
	id_kp = quotes[0].contents[0].get('data-url')
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
		print("-- everything is ok with the request for IMDb --")
	elif response.status_code == 404:
		print('-- not found --')
	else:
		print("-- something is wrong --",response.status_code)
	
	soup = BeautifulSoup(response.content, "html.parser")

	quotes = soup.find_all('table', class_='findList')
	quotes_cool = quotes[0].contents[1].contents[1].contents[1]
	id_imdb = quotes_cool.get('href')
	url_imdb =  'https://www.imdb.com' + str(id_imdb)
	return url_imdb

def main(name):
	url_kp = find_url_kp(name)
	ru_name,eng_name,release_year,country,producer,runtime,genre,rating_kp,actor,storyline = kp_info(url_kp)
	url_imdb = find_url_imdb(eng_name)
	rating_imdb = imdb_info(url_imdb)

	print_info(ru_name,eng_name,release_year,country,producer,runtime,genre,rating_kp,rating_imdb,actor,storyline)

if __name__ == '__main__':
	name = ''
	main(name)