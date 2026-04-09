"""
seeder.py — создание таблиц и наполнение виртуального склада тестовыми данными

Запускается один раз перед стартом системы
Если БД уже существует — пересоздаёт таблицы заново

Использование:
    python -m seeder.seeder
"""

import random
import uuid

from database import get_connection # noqa
from seeder.fixtures import CELLS, PRODUCTS # noqa


def create_tables(cursor: object) -> None:
    """
    Если есть старые таблицы - удалить
    Создать таблицы cells и eos
    """

    cursor.executescript("""
        DROP TABLE IF EXISTS eos;
        DROP TABLE IF EXISTS cells;

        CREATE TABLE cells (
            cell_id    TEXT PRIMARY KEY,
            capacity   INTEGER NOT NULL,
            is_blocked INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE eos (
            eo_id           TEXT PRIMARY KEY,
            product         TEXT NOT NULL,
            material_id     TEXT NOT NULL,
            batch           TEXT NOT NULL,
            production_date TEXT NOT NULL,
            quantity        INTEGER NOT NULL,
            weight_kg       REAL NOT NULL,
            cell_id         TEXT NOT NULL REFERENCES cells(cell_id),
            is_reserved     INTEGER NOT NULL DEFAULT 0,
            reservation_id  TEXT
        );
    """)


def seed_cells(cursor: object) -> None:
    """Заполнить таблицу cells из fixtures.CELL"""

    cursor.executemany(
        "INSERT INTO cells (cell_id, capacity, is_blocked) VALUES (:cell_id, :capacity, :is_blocked)",
        CELLS
    )


def seed_eos(cursor: object) -> None:
    """
    Заполнить таблицу eos случайными данными
    Каждая ячейка получает от 5 до 16 ЕО одного продукта из fixtures.PRODUCTS
    """

    for cell in CELLS:
        product = random.choice(PRODUCTS)
        eo_count = random.randint(9, 16)

        for _ in range(eo_count):
            eo_id = str(uuid.uuid4())
            cursor.execute(
                """
                INSERT INTO eos (
                    eo_id, product, material_id, batch,
                    production_date, quantity, weight_kg,
                    cell_id, is_reserved, reservation_id
                ) VALUES (
                    :eo_id, :product, :material_id, :batch,
                    :production_date, :quantity, :weight_kg,
                    :cell_id, :is_reserved, :reservation_id
                )
                """,
                {
                    "eo_id": eo_id,
                    "product": product["product"],
                    "material_id": product["material_id"],
                    "batch": product["batch"],
                    "production_date": product["production_date"],
                    "quantity": product["quantity"],
                    "weight_kg": product["weight_kg"],
                    "cell_id": cell["cell_id"],
                    "is_reserved": 0,
                    "reservation_id": None,
                }
            )


def run() -> None:
    """Точка входа seeder"""

    with get_connection() as conn:
        cursor = conn.cursor()
        create_tables(cursor)
        seed_cells(cursor)
        seed_eos(cursor)
        conn.commit()

    print("БД создана и заполнена.")


if __name__ == "__main__":
    run()