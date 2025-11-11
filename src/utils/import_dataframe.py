import pandas as pd
from typing import Literal

DATASET = Literal[
    "customer",
    "geolocation",
    "order_items",
    "order_payments",
    "order_reviews",
    "orders",
    "products",
    "sellers",
    "product_category_name",
]


def import_dataframe(df: DATASET) -> pd.DataFrame:
    key = {
        "customer": "../database/olist_customers_dataset.csv",
        "geolocation": "../database/olist_geolocation_dataset.csv",
        "order_items": "../database/olist_order_items_dataset.csv",
        "order_payments": "../database/olist_order_payments_dataset.csv",
        "order_reviews": "../database/olist_order_reviews_dataset.csv",
        "orders": "../database/olist_orders_dataset.csv",
        "products": "../database/olist_products_dataset.csv",
        "sellers": "../database/olist_sellers_dataset.csv",
        "product_category_name": "../database/product_category_name_translation.csv",
    }

    path = key[df]

    return pd.read_csv(path)
