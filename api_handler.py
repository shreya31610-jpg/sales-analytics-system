import requests

def fetch_all_products():
    try:
        response = requests.get("https://dummyjson.com/products?limit=100", timeout=10)
        data = response.json()
        return data.get("products", [])
    except:
        return []


def create_product_mapping(api_products):
    mapping = {}

    for p in api_products:
        pid = p.get("id")

        if pid is not None:
            mapping[pid] = {
                "category": p.get("category"),
                "brand": p.get("brand"),
                "rating": p.get("rating")
            }

    return mapping


def enrich_sales_data(transactions, product_mapping):
    enriched = []

    for t in transactions:
        # Example ProductID = P101 -> numeric id = 101
        product_id_str = t.get("ProductID", "")

        try:
            numeric_id = int(product_id_str[1:])
            api_data = product_mapping.get(numeric_id)

            t["API_Category"] = api_data["category"] if api_data else None
            t["API_Brand"] = api_data["brand"] if api_data else None
            t["API_Rating"] = api_data["rating"] if api_data else None
            t["API_Match"] = True if api_data else False

        except:
            t["API_Category"] = None
            t["API_Brand"] = None
            t["API_Rating"] = None
            t["API_Match"] = False

        enriched.append(t)

    return enriched
import requests

def fetch_all_products():
    try:
        response = requests.get("https://dummyjson.com/products?limit=100", timeout=10)
        data = response.json()
        return data.get("products", [])
    except:
        return []


def create_product_mapping(api_products):
    mapping = {}

    for p in api_products:
        pid = p.get("id")

        if pid is not None:
            mapping[pid] = {
                "category": p.get("category"),
                "brand": p.get("brand"),
                "rating": p.get("rating")
            }

    return mapping


def enrich_sales_data(transactions, product_mapping):
    enriched = []

    for t in transactions:
        # Example ProductID = P101 -> numeric id = 101
        product_id_str = t.get("ProductID", "")

        try:
            numeric_id = int(product_id_str[1:])
            api_data = product_mapping.get(numeric_id)

            t["API_Category"] = api_data["category"] if api_data else None
            t["API_Brand"] = api_data["brand"] if api_data else None
            t["API_Rating"] = api_data["rating"] if api_data else None
            t["API_Match"] = True if api_data else False

        except:
            t["API_Category"] = None
            t["API_Brand"] = None
            t["API_Rating"] = None
            t["API_Match"] = False

        enriched.append(t)

    return enriched
