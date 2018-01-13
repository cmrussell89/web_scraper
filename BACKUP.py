from flask import Flask, redirect, render_template
import sqlite3
from forms import SearchForm
from flask_bootstrap import Bootstrap
from scraper import scrape


app = Flask(__name__)
app.secret_key = 'GHJSDjhjsdu^&yd786dgaisd97'
Bootstrap(app)
conn = sqlite3.connect('scraper.db', check_same_thread=False)
c = conn.cursor()


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS supplementInfo(name TEXT UNIQUE, brand TEXT, price INTEGER, rating INTEGER)')


def data_entry():
    products = scrape()
    for each in products:
        name = each["product_name"]
        brand = each["product_brand"]
        price = each["price"]
        rating = each["rating"]
        c.execute("INSERT OR IGNORE INTO supplementInfo(name, brand, price, rating) VALUES (?, ?, ?, ?)",
              (name, brand, price, rating))
    conn.commit()


def get_products():
    c.execute("SELECT * FROM supplementInfo ORDER BY name")
    products = c.fetchall()
    return products


create_table()
data_entry()


@app.route('/', methods=('GET', 'POST'))
def index():
    show_results = 'all'
    products = get_products()
    form = SearchForm()

    if form.validate_on_submit():
        show_results = 'searched'
        item = '%' + form.searchFor.data + '%'
        c.execute("SELECT * FROM supplementInfo WHERE (name) LIKE (?) OR (brand) LIKE (?)", (item, item))
        search_results = c.fetchall()

        choice = form.orderBy.data
        if choice == 'name':
            show_results = 'sorted'
            c.execute("SELECT * FROM supplementInfo ORDER BY name")
            sorted_products = c.fetchall()
        elif choice == 'brand':
            show_results = 'sorted'
            c.execute("SELECT * FROM supplementInfo ORDER BY brand")
            sorted_products = c.fetchall()
        elif choice == 'price':
            show_results = 'sorted'
            c.execute("SELECT * FROM supplementInfo ORDER BY cast(price as money) ASC")
            sorted_products = c.fetchall()
        else:
            show_results = 'sorted'
            c.execute("SELECT * FROM supplementInfo ORDER BY cast(rating as decimal) DESC")
            sorted_products = c.fetchall()
            return render_template('index.html', sorted_products=sorted_products, form=form, show_results=show_results)
    else:
        return render_template('index.html', products=products, form=form, show_results=show_results)




if __name__ == "__main__":
    app.run()
