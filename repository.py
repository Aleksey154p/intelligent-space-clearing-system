"""
repository.py - запросы к БД

Единственный модуль который работает с SQL напрямую
Возвращает объекты моделей, не сырые данные

Использование:
    from repository import Repository
    repo = Repository()
    cells = repo.get_cells_by_range("P100", "P120")
    all_cells = repo.get_all_cells()
"""

from database import get_connection
from models import EO, Cell


class Repository:

    def _build_cells(self, rows: list) -> list[Cell]:
        """
        Собрать список Cell из строк JOIN-запроса

        Каждая строка содержит данные ячейки + одно ЕО
        Одна ячейка = много строк (по числу ЕО)

        Порядок сборки:
            1. Идём по строкам
            2. Если ячейка новая — создаём Cell
            3. Добавляем eo_id в cell.eo_list
        """
        cells: dict[str, Cell] = {}

        for row in rows:
            cell_id = row["cell_id"]

            if cell_id not in cells:
                cells[cell_id] = Cell(
                    cell_id=cell_id,
                    capacity=row["capacity"],
                    is_blocked=bool(row["is_blocked"]),
                )

            if row["eo_id"] is not None:
                # JOIN даёт все поля ЕО — собираю полный объект
                eo = EO(
                    eo_id=row["eo_id"],
                    product=row["product"],
                    material_id=row["material_id"],
                    batch=row["batch"],
                    production_date=row["production_date"],
                    quantity=row["quantity"],
                    weight_kg=row["weight_kg"],
                    cell_id=cell_id,
                    is_reserved=bool(row["is_reserved"]),
                    reservation_id=row["reservation_id"],
                )
                cells[cell_id].eo_list.append(eo)

        return list(cells.values())

    def get_cells_by_range(self, start: str, end: str) -> list[Cell]:
        """
        Получить ячейки диапазона с заполненными eo_list
        Один запрос через LEFT JOIN

        Использование:
            repo = Repository()
            repo.get_cells_by_range("P100", "P120")  # → list[Cell]
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                    SELECT c.cell_id, c.capacity, c.is_blocked,
                    e.eo_id, e.product, e.material_id, e.batch,
                    e.production_date, e.quantity, e.weight_kg,
                    e.is_reserved, e.reservation_id
                    FROM cells c
                    LEFT JOIN eos e ON e.cell_id = c.cell_id
                    WHERE c.cell_id >= :start AND c.cell_id <= :end
                    ORDER BY c.cell_id
                    """,
                {"start": start, "end": end}
            )
            rows = cursor.fetchall()

        return self._build_cells(rows)

    def get_all_cells(self) -> list[Cell]:
        """
        Получить все ячейки склада с заполненными eo_list
        Используется solver для поиска целевых ячеек

        Использование:
            repo = Repository()
            repo.get_all_cells()  # → list[Cell]
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT c.cell_id, c.capacity, c.is_blocked,
                e.eo_id, e.product, e.material_id, e.batch,
                e.production_date, e.quantity, e.weight_kg,
                e.is_reserved, e.reservation_id
                FROM cells c
                LEFT JOIN eos e ON e.cell_id = c.cell_id
                ORDER BY c.cell_id
                """
            )
            rows = cursor.fetchall()

        return self._build_cells(rows)