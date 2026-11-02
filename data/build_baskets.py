"""Write data/baskets.csv and data/products.csv: the shopping baskets of an online shop.

The source is the Online Retail II spreadsheet of the UCI Machine Learning Repository, two years
of invoices from a British gift wholesaler. It is 43 MB and holds a million order lines, far more
than a notebook needs, so this script keeps only what notebook 03 reads: one row per basket with
the stock codes it contained, and one row per product with its description.

Cancellations, returns and single-item baskets go, since none of them says anything about which
products are bought together, and so do baskets of more than sixty products: the largest invoice
in the file has 1,108 lines, which is a wholesaler restocking rather than somebody shopping, and
keeping those made every recommendation vaguer. The spreadsheet is downloaded rather than
committed; the two CSVs it produces are what the repository ships.

Run from the repository root: uv run --with openpyxl python data/build_baskets.py
"""

import io
import zipfile
from pathlib import Path
from urllib.request import urlopen

import pandas as pd

DATA = Path(__file__).parent
SOURCE = "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"
MIN_BASKET = 2   # one product says nothing about what goes with what
MAX_BASKET = 60  # above this it is a wholesale order, not a shopping trip, and it only adds noise


def download_orders():
    """Return the order lines of both sheets of the Online Retail II spreadsheet."""
    with urlopen(SOURCE) as response:
        archive = zipfile.ZipFile(io.BytesIO(response.read()))
    name = next(member for member in archive.namelist() if member.endswith(".xlsx"))
    sheets = pd.read_excel(archive.open(name), sheet_name=None, dtype={"Invoice": str, "StockCode": str})
    return pd.concat(sheets.values(), ignore_index=True)


def clean(orders):
    """Return the order lines that record a purchase, with tidy codes and descriptions."""
    orders = orders.dropna(subset=["Invoice", "StockCode", "Description"]).copy()
    orders["Invoice"] = orders["Invoice"].str.strip()
    orders["StockCode"] = orders["StockCode"].str.strip().str.upper()
    orders["Description"] = orders["Description"].str.strip().str.replace(r"\s+", " ", regex=True)
    orders = orders[~orders["Invoice"].str.startswith("C")]  # C marks a cancelled invoice
    return orders[orders["Quantity"] > 0]


def baskets_of(orders):
    """Return one row per invoice: the stock codes it contained, in order, as one string."""
    grouped = orders.groupby("Invoice")["StockCode"].apply(lambda codes: " ".join(dict.fromkeys(codes)))
    basket = grouped.reset_index().rename(columns={"Invoice": "invoice", "StockCode": "items"})
    size = basket["items"].str.split().str.len()
    return basket[size.between(MIN_BASKET, MAX_BASKET)]


def products_of(orders, baskets):
    """Return one row per stock code in `baskets`: the description it is sold under most often.

    A code is listed under several spellings over two years, so the most frequent one wins. Codes
    that only ever appeared in a dropped basket are left out, so the catalogue has no dead rows.
    """
    kept = set(" ".join(baskets["items"]).split())
    counted = orders.groupby(["StockCode", "Description"]).size().rename("lines").reset_index()
    counted = counted[counted["StockCode"].isin(kept)]
    best = counted.sort_values("lines", ascending=False).drop_duplicates("StockCode")
    return best[["StockCode", "Description"]].rename(
        columns={"StockCode": "code", "Description": "description"}).sort_values("code")


if __name__ == "__main__":
    orders = clean(download_orders())
    baskets = baskets_of(orders)
    products = products_of(orders, baskets)
    baskets.to_csv(DATA / "baskets.csv", index=False)
    products.to_csv(DATA / "products.csv", index=False)
    sizes = baskets["items"].str.split().str.len()
    print(f"{len(baskets):,} baskets, {sizes.sum():,} items, median basket {int(sizes.median())}")
    print(f"{len(products):,} products")
