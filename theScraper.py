import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
    # Add more if needed
]

headers = {
    'User-Agent': random.choice(user_agents)
}

base_url = 'https://www.goodreads.com'
list_url = 'https://www.goodreads.com/list/show/1.Best_Books_Ever?page=1'

response = requests.get(list_url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

books = []

for book in soup.select('tr[itemtype="http://schema.org/Book"]'):
    try:
        title = book.select_one('a.bookTitle').get_text(strip=True)
        author = book.select_one('a.authorName').get_text(strip=True)
        rating = book.select_one('span.minirating').get_text(strip=True)

        # Link to the book's detail 
        book_link = base_url + book.select_one('a.bookTitle')['href']
        book_page = requests.get(book_link, headers=headers)
        book_soup = BeautifulSoup(book_page.content, 'html.parser')

        books.append({
            'Title': title,
            'Author': author,
            'Rating': rating,
        })

        time.sleep(1)  # Optional: To avoid hammering the site too fast

    except Exception as e:
        print(f"Error: {e}")
        continue

df = pd.DataFrame(books)
df.to_json('goodreads_books.json', orient='records', lines=False, indent=4) 

print(df.head())
