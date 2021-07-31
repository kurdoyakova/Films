import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/88.0.4324.150 Safari/537.36",
"Accept-language":"ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,\
*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"}


class Film():
    """Class for describing film info"""
    def __init__(self):
        self.type_genre = 'фильм'
        self.release_year = ''
        self.ru_name = ''
        self.eng_name = ''
        self.rating_kp = ''
        self.rating_imdb = ''
        self.runtime = ''
        self.genre = []
        self.country = []
        self.producer = []
        self.storyline = ''
        self.actor = []

    def __repr__(self):
        attributes = self.__dict__
        table = []
        for k, v in attributes.items():
            table.append([str(k), v])
        return tabulate(table, tablefmt="plain")


class Serial(Film):
    """Class for describing serial info"""
    def __init__(self):
        super().__init__()
        self.type_genre = 'сериал'
        self.number_of_seasons = ''


def resnonse_url(url):
    """receiving a response from the server"""
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("-- works --")
    elif response.status_code == 404:
        print('-- not found --')
    else:
        print("-- something is wrong --", response.status_code)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def kp_type(url):
    """type definition"""
    soup = resnonse_url(url)
    quotes_for_type = soup.find_all('div', class_='styles_title__1yvs9')
    if quotes_for_type == []:
        quotes_for_type = soup.find_all('div', class_='styles_title__3tVSa')
        type_with_year = quotes_for_type[0].contents[0].contents[2].text
        type_genre = type_with_year[1:7]
    else:
        type_genre = 'фильм'
    return type_genre, soup


def kp_info_film(soup):
    """getting basic information about a movie on the kinopoisk"""
    film = Film()
    quotes = soup.find_all(
        'div', class_="styles_rowDark__2qC4I styles_row__2ee6F")
    if quotes == []:
        quotes = soup.find_all(
            'div', class_='styles_rowLight__3uy9z styles_row__2ee6F')
    quotes2 = soup.find_all('div', class_='styles_title__1yvs9')
    quotes3 = soup.find_all('div', class_='styles_body__2Ynqg')
    quotes4 = soup.find_all('div', class_='styles_filmSynopsis__zLClu')
    quotes5 = soup.find_all('div', class_="styles_actors__2zt1j")

    film.release_year = (quotes[0].contents)[1].text
    ru_name_with_year = (quotes2[0].contents)[0].contents[0].text
    film.ru_name = ru_name_with_year[:len(ru_name_with_year)-6]
    film.eng_name = (quotes2[0].contents)[1].contents[0].text
    film.rating_kp = (quotes3[0].contents)[0].text

    runtime_full = (quotes[len(quotes)-1].contents)[1].text
    for i in runtime_full:
        if i == '/':
            film.runtime = runtime_full[len(runtime_full)-6:len(runtime_full)]
            break
        film.runtime = runtime_full[0:len(runtime_full)-1]

    genres = (quotes[2].contents)[1].contents[0].contents
    for i in range(0, len(genres), 2):
        film.genre.append(genres[i].text)

    countrys = quotes[1].contents[1].contents
    for i in range(0, len(countrys), 2):
        film.country.append(countrys[i].text)

    producers = (quotes[4].contents)[1].contents
    for i in range(0, len(producers), 2):
        if producers[i].text == '...':
            break
        film.producer.append(producers[i].text)

    if quotes4 == []:
        film.storyline = '-'
    else:
        film.storyline = quotes4[0].text

    actors = (quotes5[0].contents)[1].contents
    for i, _ in enumerate(actors):
        film.actor.append(actors[i].text)

    return film


def kp_info_serial(soup):
    """getting basic information about the series on the kinopoisk"""
    serial = Serial()
    quotes = soup.find_all(
        'div', class_="styles_rowDark__2qC4I styles_row__2ee6F")
    if quotes == []:
        quotes = soup.find_all(
            'div', class_='styles_rowLight__3uy9z styles_row__2ee6F')
    quotes2 = soup.find_all('div', class_='styles_title__3tVSa')
    quotes3 = soup.find_all('div', class_='styles_body__2Ynqg')
    quotes4 = soup.find_all('div', class_='styles_filmSynopsis__zLClu')
    quotes5 = soup.find_all('div', class_="styles_actors__2zt1j")

    release_year_with_number_of_seasons = (quotes[0].contents)[1].text
    serial.release_year = release_year_with_number_of_seasons[0:4]
    serial.number_of_seasons = release_year_with_number_of_seasons[6:7]
    serial.ru_name = (quotes2[0].contents)[0].contents[0].text
    serial.eng_name = (quotes2[0].contents)[1].contents[0].text
    serial.rating_kp = (quotes3[0].contents)[0].text

    runtime_full = (quotes[len(quotes)-1].contents)[1].text
    for i in runtime_full:
        if i == '/':
            serial.runtime = runtime_full[len(runtime_full)-6:len(runtime_full)]
            break
        serial.runtime = runtime_full[0:len(runtime_full)-1]

    countrys = quotes[1].contents[1].contents
    for i in range(0, len(countrys), 2):
        serial.country.append(countrys[i].text)

    genres = (quotes[2].contents)[1].contents[0].contents
    for i in range(0, len(genres), 2):
        serial.genre.append(genres[i].text)

    producers = (quotes[4].contents)[1].contents
    for i in range(0, len(producers), 2):
        if producers[i].text == '...':
            break
        serial.producer.append(producers[i].text)

    if quotes4 == []:
        serial.storyline = '-'
    else:
        serial.storyline = quotes4[0].text

    actors = (quotes5[0].contents)[1].contents
    for i, _ in enumerate(actors):
        serial.actor.append(actors[i].text)

    return serial


def imdb_info(url):
    """getting basic information on the IMDb website"""
    soup = resnonse_url(url)
    quotes_for_rating_imdb = soup.find_all(
        'div', class_="AggregateRatingButton__ContentWrap-sc-1ll29m0-0 hmJkIS")
    rating_imdb = (quotes_for_rating_imdb[0].contents)[0].contents[0].text
    return rating_imdb


def find_url_kp(name):
    """getting url on the kinopoisk"""
    words = name.split()
    name_like_url = words[0]
    for i in range(1, len(words)):
        name_like_url = str(name_like_url) + '+' + str(words[i])
    url = 'https://www.kinopoisk.ru/index.php?kp_query=' + str(name_like_url)
    soup = resnonse_url(url)
    quotes_for_id_kp = soup.find_all('p', class_='name')
    id_kp = quotes_for_id_kp[0].contents[0].get('data-url')
    url_kp = 'https://www.kinopoisk.ru' + str(id_kp)
    return url_kp


def find_url_imdb(name):
    """getting url on the IMDb"""
    words = name.split()
    name_like_url = words[0]
    for i in range(1, len(words)):
        name_like_url = str(name_like_url) + '+' + str(words[i])
    url = 'https://www.imdb.com/find?q=' + \
        str(name_like_url) + '&ref_=nv_sr_sm'
    soup = resnonse_url(url)
    quotes_for_id_imdb = soup.find_all('table', class_='findList')
    quotes_cool = quotes_for_id_imdb[0].contents[1].contents[1].contents[1]
    id_imdb = quotes_cool.get('href')
    url_imdb = 'https://www.imdb.com' + str(id_imdb)
    return url_imdb


def main(name):
    """the main task"""
    url_kp = find_url_kp(name)
    type_genre, soup = kp_type(url_kp)
    if type_genre == 'фильм':
        film = kp_info_film(soup)
        url_imdb = find_url_imdb(film.eng_name)
        film.rating_imdb = imdb_info(url_imdb)
        print(film)
    else:
        serial = kp_info_serial(soup)
        url_imdb = find_url_imdb(serial.eng_name)
        serial.rating_imdb = imdb_info(url_imdb)
        print(serial)


if __name__ == '__main__':
    NAME = 'рик и морти'
    main(NAME)
