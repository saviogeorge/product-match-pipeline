from db import products_collection

def get_product_by_id(product_id):
    return products_collection.find_one({"_id": product_id})

def get_products_by_category(category):
    return list(products_collection.find({"category": category}))

def get_products_under_price(max_price):
    return list(products_collection.find({"price": {"$lt": max_price}}))
