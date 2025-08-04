from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/')
def scrape_books():
    url = 'https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html'

    response = requests.get(url)

    soup = BeautifulSoup(response.content,'html.parser')

    books = soup.find_all('li',{'class':'col-xs-6 col-sm-4 col-md-3 col-lg-3'})

    books_data = []

    for book in books:
        name = book.find('h3').find('a')
        price = book.find("div",class_="product_price").find('p')

        name =  name.get('title') if name else None
        price = price.get_text(strip=True) if price else None
        books_data.append([name,price])
    
    df = pd.DataFrame(books_data,columns=['Name','Price'])
    return render_template("index.html",table=df.to_html(index=False,classes="table table-striped"))


if __name__ == '__main__':
    app.run(debug=True, port=3000)