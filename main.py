import requests
from bs4 import BeautifulSoup
import random
from flask import Flask, render_template, redirect, url_for, flash, request, abort

app = Flask(__name__)
all_genres = ['Classics', 'Comics', 'Fantasy', 'Fiction', 'Horror', 'Humor', 'Mystery', 'Nonfiction', 'Philosophy',' Romance', 'Science', 'Suspense', 'Thriller', 'Travel', 'Young Adult']

def get_details(choice):
    URL = "https://www.goodreads.com/"
    genre = choice
    contents = requests.get(f'{URL}shelf/show/{genre}')
    soup = BeautifulSoup(contents.text, "html.parser")
    items = soup.find_all('a', class_="leftAlignedImage")[:20]
    item = random.choice(items)

    book_title = item['title']
    book_link = item['href']

    book = requests.get(f'{URL}{book_link}')
    soup = BeautifulSoup(book.text, "html.parser")

    book_rating = soup.find_all('span', attrs={'itemprop':"ratingValue"})[0].text
    book_author = soup.find_all('a', class_="authorName")[0].text
    book_img = soup.find_all('img', id="coverImage")[0]['src']
    book_description = soup.find_all('div', id="descriptionContainer")[0].find_all('span')

    book_rating = ''.join(book_rating.split())
    book_description = book_description[1].text
    # print(book_title, book_author, ''.join(book_rating.split()))
    # print(book_description[1].text)
    return ([book_title, book_author, book_rating, book_description, book_img ])


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html', genre=all_genres)

@app.route('/find', methods=['GET', 'POST'])
def find():
    select = request.form.get('sel1')
    print(str(select))
    all_details = get_details(select)
    return render_template('book.html', details=all_details)

if __name__ == "__main__":
    app.run(debug=True)