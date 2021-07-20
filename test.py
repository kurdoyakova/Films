import requests
from bs4 import BeautifulSoup

# url = 'https://www.kinopoisk.ru/film/61333/'
url = 'https://www.kinopoisk.ru/film/195408/'

headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
"Accept-language":"ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}

response = requests.get(url, headers = headers)
if response.status_code == 200:
	print("-- everything is ok with the request --")
else:
	print("-- something is wrong --",response.status_code)

soup = BeautifulSoup(response.content, "html.parser")

quotes = soup.find_all('div', class_='styles_rowLight__3uy9z styles_row__2ee6F')

release_year = (quotes[0].contents)[1].text
country = (quotes[1].contents)[1].text
genre = (quotes[2].contents)[1].text
producer = (quotes[4].contents)[1].text
runtime = (quotes[22].contents)[1].text

quotes2 = soup.find_all('div', class_='styles_title__1yvs9')

ru_name_with_year = (quotes2[0].contents)[0].text
ru_name = ru_name_with_year[:len(ru_name_with_year)-6]
eng_name = (quotes2[0].contents)[1].contents[0].text

print(ru_name)