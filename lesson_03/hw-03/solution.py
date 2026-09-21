"""
ПР-01: Каталог товаров.
Чтение — из shop, изменения — в sandbox.
"""

from pymongo import MongoClient
from pymongo.errors import BulkWriteError

client = MongoClient("mongodb://localhost:27017")
shop_products = client["shop"]["products"]
sandbox_products = client["sandbox"]["products"]


# ============================================================
# ЗАДАЧА 1: Витрина каталога
# ============================================================

def catalog_page(category=None, page=1, limit=5):
    query = {}
    if category:
        query["category"] = category

    projection = {"sku": 1, "title": 1, "price": 1, "rating": 1, "_id": 0}
    cursor = (
        shop_products.find(query, projection)
        .sort([("price", 1), ("sku", 1)])
        .skip((page - 1) * limit)
        .limit(limit)
    )
    return list(cursor), shop_products.count_documents(query)


# ============================================================
# ЗАДАЧА 2: Приёмка поставки
# ============================================================

def accept_delivery():
    print("\n" + "=" * 60)
    print("ПРИЁМКА ПОСТАВКИ")
    print("=" * 60)

    # --- Шаг 1: выставить qty_total трём артикулам ---
    totals = {
        "SKU-NB-001": 5,
        "SKU-PH-006": 12,
        "SKU-PR-010": 3,
    }
    print("\n--- Шаг 1: остатки (qty_total) ---")
    for sku, total in totals.items():
        r = sandbox_products.update_one(
            {"sku": sku},
            {"$set": {"qty_total": total}}
        )
        mark = "[+]" if r.matched_count else "[!]"
        print(f"  {mark} {sku}: qty_total = {total}")

    # --- Шаг 2: завести две новые позиции ---
    new_items = [
        {
            "_id": "p-101",
            "sku": "SKU-AC-101",                       # ← было SKU-NB-099
            "title": "Чехол для ноутбука 14\"",         # ← было 'Ноутбук UltraBook 14"'
            "brand": "UltraBook",
            "category": "аксессуары",                  # ← было "ноутбуки"
            "price": 3500,                             # ← было 89000
            "specs": ["нейлон", "чёрный"],
            "stock": [{"warehouse": "Санкт-Петербург", "qty": 2}],
            "qty_total": 2,
            "rating": 4.7,
            "reviews": 0,
        },
        {
            "_id": "p-102",
            "sku": "SKU-AC-099",
            "title": "Мышь беспроводная",
            "brand": "Generic",
            "category": "аксессуары",
            "price": 2500,
            "specs": ["чёрная", "USB-C"],
            "stock": [{"warehouse": "Санкт-Петербург", "qty": 15}],
            "qty_total": 15,
            "rating": 4.3,
            "reviews": 0,
        },
    ]
    print("\n--- Шаг 2: новые позиции ---")
    try:
        r = sandbox_products.insert_many(new_items, ordered=False)
        print(f"  [+] Добавлено: {len(r.inserted_ids)}")
    except BulkWriteError as exc:
        print(f"  [+] Добавлено: {exc.details.get('nInserted', 0)} "
              f"(остальные уже были)")

    # --- Шаг 3: снять с продажи SKU-CP-018 ---
    print("\n--- Шаг 3: снятие SKU-CP-018 ---")
    n = sandbox_products.count_documents({"sku": "SKU-CP-018"})
    print(f"  Найдено: {n}")
    if n:
        r = sandbox_products.delete_many({"sku": "SKU-CP-018"})
        print(f"  [-] Удалено: {r.deleted_count}")

    # --- Шаг 4: бесплатная доставка аксессуарам ---
    print("\n--- Шаг 4: free_shipping аксессуарам ---")
    r = sandbox_products.update_many(
        {"category": "аксессуары"},
        {"$set": {"free_shipping": True}}
    )
    print(f"  [+] Обновлено: {r.modified_count}")

    # --- Итог ---
    print("\nИТОГ:")
    print(f"  Всего в sandbox: {sandbox_products.count_documents({})}")
    print(f"  Аксессуаров: {sandbox_products.count_documents({'category': 'аксессуары'})}")
    print(f"  free_shipping: {sandbox_products.count_documents({'free_shipping': True})}")


# ============================================================
# ТОЧКА ВХОДА
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("ВИТРИНА КАТАЛОГА")
    print("=" * 60)

    items, total = catalog_page(page=1, limit=5)
    print(f"\nСтраница 1 (всего {total}):")
    for it in items:
        print(f"  {it['sku']:12} {it['title']:35} {it['price']:>8} ₽  ★{it['rating']}")

    items, total = catalog_page(category="ноутбуки", page=1, limit=5)
    print(f"\nНоутбуки (всего {total}):")
    for it in items:
        print(f"  {it['sku']:12} {it['title']:35} {it['price']:>8} ₽  ★{it['rating']}")

    accept_delivery()