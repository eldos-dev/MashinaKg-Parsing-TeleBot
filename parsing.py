from bs4 import BeautifulSoup
import requests
import json
import lxml

# Функция принимает url, возвращает html text
def get_html(url):
    user_agent = {"User-Agent":"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
    response = requests.get(url, headers=user_agent)
    return response.text

# Принимает data и записывает в json файл
def write_to_json(data):
    with open('mashina_kg.json', 'w') as json_file:
        json.dump(data, json_file, indent=3)

# Принимает html text, парсит нужные информации и вызывает функцию write_to_json для записи в  файл json
def get_data_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    wrap_div = soup.find('div', class_='search-results-table').find('div', class_='table-view-list')
    products = wrap_div.find_all('div', class_='list-item list-label')

    list_data = []
    for product in products:
        try:
            title = product.find('a').find('h2').text.strip()
        except:
            title = ''
        try:
            image = product.find('img').get('data-src').strip()
        except:
            image = ''
        try:
            price = product.find('p', class_='price').find('strong').text
            year = product.find('p', class_='year-miles').find('span').text.strip()
            fuel = product.find('p', class_='body-type').text.strip()
            wheel = product.find('p', class_='volume').text.strip()
            # city = product.find('p', class_='city').text.strip()
            description = {
                            'price': price,
                            'year': year,
                            'fuel': fuel, 
                            'wheel': wheel}
        except:
            description = ''
        
        data = {
                'title': title,
                'image': image,
                'description': description}
        list_data.append(data)
    write_to_json(list_data)

# Очищаем csv файл перед записанием информаци.
def clean_json_file():
    with open('mashina_kg.json', 'w') as my_empty_json_file:
            my_empty_json_file.write('')


def main():
    special_cars_url = 'https://www.mashina.kg/specsearch/all/'

    get_data_pages(get_html(special_cars_url))


clean_json_file()
main()