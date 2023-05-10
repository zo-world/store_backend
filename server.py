from flask import Flask, request, abort
import json
from config import db
from flask_cors import CORS

app = Flask(__name__)
CORS(app) #disable CORS security rule

@app.get("/")
def home():
    return "Hello from Flask"

@app.get("/test")
def test():
    return "This is another page"


###### API ENDPOINTS ########
######       JSON    ########

def fix_id(obj):
    # fix the object to be json parsable
    obj["_id"] = str(obj["_id"])
    return obj

@app.get("/api/about")
def about():
    me = { "name": "Yreish Pozo" }
    return json.dumps(me)

@app.get("/api/catalog")
def get_catalog():
    products = []
    cursor = db.products.find({})
    for prod in cursor:
        products.append(fix_id(prod))

    return json.dumps(products)

@app.get("/api/total")
def total_value():
    cursor = db.products.find({})
    total = 0
    for prod in cursor:
        total += prod["price"]

    return json.dumps(total)

@app.get("/api/products")
def count_products():
    cursor = db.products.find({})
    count = 0
    for prod in cursor:
        count += 1

    return json.dumps(count) 

@app.post("/api/catalog")
def save_product():
    data = request.get_json()
    db.products.insert_one(data)

    print(data) # to terminal

    return json.dumps(fix_id(data))



@app.get("/api/categories")
def get_categories():
    categories = []
    cursor = db.products.find({})
    for prod in cursor:
        cat = prod["category"]
        if cat not in categories:
            categories.append(cat)

    return json.dumps(categories)

# get the list of products that belong to given category
@app.get("/api/products/category/<name>")
def get_by_category(name):
    results = []
    cursor = db.products.find({"category": name})
    for prod in cursor:
        results.append(fix_id(prod))
    
    return json.dumps(results)

@app.get("/api/products/search/<term>")
def search_products(term):
    results = []
    cursor = db.products.find({"title": {"$regex": term, "$options": "i"} })
    for prod in cursor:
        results.append(fix_id(prod))

    return json.dumps(results)




# get /api/products/lower/value
# to retrieve all products whose is lower than given value

@app.get("/api/products/lower/value")
def price_lower(value):
    results = []
    cursor = db.products.find({"price": {"$lt": float(value)}})
    for prod in cursor:
        results.append(fix_id(prod))
    
    return json.dumps(results)


#get /api;/products/greater/value
#greater or equal
@app.get("/api/products/greater/value")
def price_greater(value):
    results = []
    cursor = db.products.find({"price": {"$gte": float(value)}})
    for prod in cursor:
        results.append(fix_id(prod))
    
    return json.dumps(results)



####################################
##### COUPON CODES #################
####################################

#GET /api/coupons -> retrieve all
#POST /api/coupons -> saave new
# GET /api/coupons/code -> retrieve 1 by code

@app.post("/api/coupons")
def save_coupons():
    data = request.get_json()
    db.coupons.insert_one(data)

    return json.dumps(fix_id(data))


@app.get("/api/coupons")
def get_coupons():
    results = []
    cursor = db.coupons.find({})
    for coupon in cursor:
        results.append(fix_id(coupon))
    
    return json.dumps(results)

@app.get("/api/coupons/<code>")
def coupon_by_code(code):
    coupon = db.coupons.find_one({"code": code})
    if not coupon:
        return abort(404, "Invalid Code")
    
    return json.dumps(fix_id(coupon))

@app.delete("/api/coupons/<code>")
def delete_coupon(code):
    db.coupons.delete_one({"code": code})
    return json.dumps({"status": "OK", "message": "Coupon deleted"})