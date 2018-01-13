import bs4 as bs
import urllib.request


def scrape():
    l = []
    urls = ['https://www.bodybuilding.com/store/whey.html', 'https://www.bodybuilding.com/store/goalpreworkout.htm', 'https://www.bodybuilding.com/store/ephfree.htm']
    for url in urls:
        sauce = urllib.request.urlopen(url).read()
        soup = bs.BeautifulSoup(sauce, 'lxml')

        all_products = soup.find_all('div', class_='product')

        for each in all_products:
            dataset = {}

            #name
            product_name = each.find('a', itemprop='name')
            product_name = product_name.text.replace('\n', "").strip()
            dataset['product_name'] = product_name

            #brand
            product_brand = each.find('div', itemprop='brand')
            product_brand = product_brand.text.replace('\n', "").strip()
            dataset['product_brand'] = product_brand

            #price
            product_price = each.find('div', class_='product__price')
            product_price = product_price.text.replace('\n', "").strip()
            product_price = product_price[1:]
            dataset['price'] = product_price

            #rating
            product_rating = each.find('span', itemprop='ratingValue')
            product_rating = product_rating.text.replace('\n', "").strip() + '/10'
            dataset['rating'] = product_rating

            l.append(dataset)

    return l


if __name__ == "__main__":
    print(scrape())