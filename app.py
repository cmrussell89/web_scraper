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
    products = get_products()
    form = SearchForm()
    if form.validate_on_submit():
        order_by = form.orderBy.data
        item = '%' + form.searchFor.data + '%'
        c.execute("SELECT * FROM supplementInfo WHERE (name) LIKE (?) OR (brand) LIKE (?) ORDER BY " + order_by, (item, item))
        search_results = c.fetchall()
        if item == "% %":
            c.execute("SELECT * FROM supplementInfo ORDER BY " + order_by)
            search_results = c.fetchall()
            return render_template('index.html', search_results=search_results, form=form)
        return render_template('index.html', search_results=search_results, form=form)
    else:
        return render_template('index.html', form=form, products=products)


if __name__ == "__main__":
    app.run(debug="TRUE")
