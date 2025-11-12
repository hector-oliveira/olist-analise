# import pandas as pd
# from typing import Literal

# DATASET = Literal[
#     "customer",
#     "geolocation",
#     "order_items",
#     "order_payments",
#     "order_reviews",
#     "orders",
#     "products",
#     "sellers",
#     "product_category_name",
# ]


# def load_dataframe(df: DATASET) -> pd.DataFrame:
#     key = {
#         "customer": "../database/olist_customers_dataset.csv",
#         "geolocation": "../database/olist_geolocation_dataset.csv",
#         "order_items": "../database/olist_order_items_dataset.csv",
#         "order_payments": "../database/olist_order_payments_dataset.csv",
#         "order_reviews": "../database/olist_order_reviews_dataset.csv",
#         "orders": "../database/olist_orders_dataset.csv",
#         "products": "../database/olist_products_dataset.csv",
#         "sellers": "../database/olist_sellers_dataset.csv",
#         "product_category_name": "../database/product_category_name_translation.csv",
#     }

#     path = key[df]

#     return pd.read_csv(path)


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


def load_dataframe(df: DATASET) -> pd.DataFrame:
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

    # Colunas que precisam ser convertidas para datetime
    parse_dates_dict = {
        "orders": [
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ],
        "order_reviews": ["review_creation_date", "review_answer_timestamp"],
    }

    path = key[df]

    # Leitura do CSV com parse_dates quando necessário
    df_loaded = pd.read_csv(path, parse_dates=parse_dates_dict.get(df, None))

    # --- Tratamentos específicos ---

    # Orders: criar flag de entrega
    if df == "orders":
        df_loaded["is_delivered"] = ~df_loaded["order_delivered_customer_date"].isnull()

    # Order reviews: preencher campos textuais ausentes
    if df == "order_reviews":
        df_loaded["review_comment_title"].fillna("Sem título", inplace=True)
        df_loaded["review_comment_message"].fillna("Sem comentário", inplace=True)

    # Products: preencher numéricos e categoria
    if df == "products":
        num_cols = [
            "product_name_lenght",
            "product_description_lenght",
            "product_photos_qty",
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm",
        ]
        for col in num_cols:
            df_loaded[col] = pd.to_numeric(df_loaded[col], errors="coerce").fillna(
                df_loaded[col].median()
            )

        # Categoria
        df_loaded["product_category_name"].fillna("desconhecido", inplace=True)
        df_loaded["product_category_name"] = df_loaded["product_category_name"].astype(
            "category"
        )

    return df_loaded
