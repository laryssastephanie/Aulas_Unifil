from flask import Flask
from bs4 import BeautifulSoup as soup
import requests

app = Flask(__name__)

@app.route('/get_dollar_today', methods=['GET'])
def get_dollar_today():
    url = 'https://economia.uol.com.br/cotacoes/cambio/'
    try:
        client_page = requests.get(url, timeout=(3.05, 27))
    except:
        return '<p>Não foi possível obter a cotação do dolar.</p>'
    page_html = client_page.text
    client_page.close()
    page_soup = soup(page_html, 'html.parser')
    dolar = page_soup.findAll('input', {'name': 'currency2'})
    return '<p>' + dolar[0]['value'] + '</p>'
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)