from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    books_data = []
    for i in range(1,3):
        url = f'https://books.toscrape.com/catalogue/page-{i}.html'

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        books = soup.find_all('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'})
        for book in books:
            name = book.find('h3').find('a').get('title')
            price = book.find("div", class_="product_price").find('p').get_text(strip=True)
            availability = book.find("p", class_="instock availability").get_text(strip=True)
            books_data.append([name, price, availability])

    now = datetime.now().strftime('%Y-%m-%d %I:%M %p')
    return render_template(
        'index.html',
        table_data=books_data,
        now=now
    )

if __name__ == '__main__':

    app.run(debug=False, port=3000, host="0.0.0.0")

    #df = pd.DataFrame(books_data,columns=['Name','Price','Availability'])
    #return render_template("index.html",table=df.to_html(index=False,classes="table table-striped"))