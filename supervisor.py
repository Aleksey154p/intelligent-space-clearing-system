"""
supervisor.py — фильтрация данных перед передачей в blender

Получает от repository:
    - ячейки диапазона (источники)
    - все ячейки склада (цели)

Фильтрует:
    - заблокированные ячейки из диапазона
    - ЕО с is_reserved=True из диапазона

Отдаёт в blender:
    - чистые ячейки источника
    - чистые ЕО источника
    - все ячейки склада (для поиска целей)
"""

from repository import Repository
from models import EO, Cell


class Supervisor:

    def __init__(self) -> None:
        self._repo = Repository()

    def get_source_cells(self, start: str, end: str) -> list[Cell]:
        """
        Получить доступные ячейки диапазона
        Исключает заблокированные и пустые

        Использование:
            sv = Supervisor()
            sv.get_source_cells("P100", "P120") → list[Cell]
        """
        cells = self._repo.get_cells_by_range(start, end)
        return [
            cell for cell in cells
            if not cell.is_blocked and cell.occupancy > 0
        ]

    def get_source_eos(self, cells: list[Cell]) -> dict[str, list[EO]]:
        """
        Получить доступные ЕО для каждой ячейки диапазона
        Исключает зарезервированные ЕО

        Возвращает словарь: cell_id → list[EO]

        Использование:
            sv = Supervisor()
            cells = sv.get_source_cells("P100", "P120")
            sv.get_source_eos(cells) → {"P101": [EO, ...], ...}
        """

        result: dict[str, list[EO]] = {}
        for cell in cells:
            available = [eo for eo in cell.eo_list if not eo.is_reserved]
            if available:
                result[cell.cell_id] = available
        return result


    def get_all_cells(self) -> list[Cell]:
        """
        Получить все ячейки склада для поиска целевых ячеек
        Исключает заблокированные

        Использование:
            sv = Supervisor()
            sv.get_all_cells() → list[Cell]
        """
        cells = self._repo.get_all_cells()
        return [cell for cell in cells if not cell.is_blocked]
