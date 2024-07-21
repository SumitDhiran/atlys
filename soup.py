import time
from typing import List
from bs4 import BeautifulSoup
import requests, json, redis
from database.database import SessionLocal, get_db
from database.models import Product
from fastapi.exceptions import HTTPException


def bulk_insert(data: List):
    db = get_db()
    db.bulk_save_objects(data)
    db.commit()

count = 0
def scrape(url: str = None, page: int = None):
    status_code, err = 201, None
    try:
        data, objs = [], []
        url = url if url else "https://dentalstall.com/shop/page/{i}/"
        limit = page if page else 100
        for i in range(1, limit+1):
            html_doc = requests.get(url.format(i=i))
            print(html_doc.status_code)
            soup = BeautifulSoup(html_doc.text, 'html.parser')
            products = soup.find_all('div',  {"class": "product-inner"})

            for product in products:
                objs.append(
                    Product(
                        product_title= product.find('img')['title'],
                        product_price=product.find('bdi').text,
                        path_to_image=product.find('img')['data-lazy-src']
                    )
                )


                data.append(
                    {
                        "product_title": product.find('img')['title'],
                        "product_price": product.find('bdi').text,
                        "path_to_image": product.find('img')['data-lazy-src']
                    }
                )

        json_data = json.dumps(data)
        # redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        if r.get("products") != json_data:
            bulk_insert(objs)
            r.set("products", json_data)
        status_code, err = 201, None
    except Exception as e:
        count += 1
        status_code, err = 400, e
        print(f"error -> {e}")
        print("retrying in 3 seconds...")
        time.sleep(3)
        if count < 10:
            scrape(url, page)

    finally:
        return (status_code, err)

