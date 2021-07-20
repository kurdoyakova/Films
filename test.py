import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
"Accept-language":"ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}

def print_info(ru_name,eng_name,release_year,country,producer,runtime,genre,rating_kp,actor,storyline):
	table = [['ru_name', ru_name], ['eng_name', eng_name], ['release_year', release_year],
		['country', country], ['producer', producer], ['runtime', runtime],
		['genres', genre], ['rating_kp', rating_kp], ['actors', actor], ['storyline', storyline]]
	print(tabulate(table, tablefmt="plain"))

def kp_info(url):	
	response = requests.get(url, headers = headers)
	if response.status_code == 200:
		print("-- everything is ok with the request --")
	else:
		print("-- something is wrong --",response.status_code)
	
	soup = BeautifulSoup(response.content, "html.parser")

	quotes = soup.find_all('div', class_='styles_rowLight__3uy9z styles_row__2ee6F')
	release_year = (quotes[0].contents)[1].text
	runtime = (quotes[22].contents)[1].text
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
	storyline = quotes4[0].text

	quotes5 = soup.find_all('div', class_="styles_actors__2zt1j")
	actor = []
	actors = (quotes5[0].contents)[1].contents
	for i in range(0,len(actors)):
		actor.append(actors[i].text)

	print_info(ru_name,eng_name,release_year,country,producer,runtime,genre,rating_kp,actor,storyline)





def main(url):
	kp_info(url)
	# imdb_info(url)

if __name__ == '__main__':
	url = 'https://www.kinopoisk.ru/film/61333/'
	# url = 'https://www.kinopoisk.ru/film/195408/'
	main(url)