"""База данных склада"""

import sqlite3

DATABASE_PATH = "virtual_warehouse.db"


def get_connection() -> sqlite3.Connection:
    """Получить подключение к БД"""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row  # результаты как словари row["cell_id"]
    return connection
