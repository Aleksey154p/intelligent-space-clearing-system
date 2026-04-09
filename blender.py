"""
blender.py — подготовка данных из supervisor для solver

Получает:
    - source_cells: list[Cell] — ячейки диапазона
    - source_eos:   dict[str, list[EO]] — доступные ЕО по ячейкам диапазона
    - all_cells:    list[Cell] — весь склад

Возвращает две структуры для solver:
    - sources:   dict — ячейки диапазона с полными данными ЕО
    - warehouse: dict — весь склад с краткими данными для поиска целей

Использование:
    from blender import Blender
    blender = Blender()
    sources, warehouse = blender.prepare(source_cells, source_eos, all_cells)
"""

from models import EO, Cell


class Blender:

    def prepare(
            self,
            source_cells: list[Cell],
            source_eos: dict[str, list[EO]],
            all_cells: list[Cell],
    ) -> tuple[dict, dict]:
        """
        Подготовить две структуры данных для solver

        Использование:
            blender = Blender()
            sources, warehouse = blender.prepare(
                source_cells, source_eos, all_cells
            )
        """
        sources = self._build_sources(source_cells, source_eos)
        warehouse = self._build_warehouse(all_cells)
        return sources, warehouse

    def _build_sources(
            self,
            source_cells: list[Cell],
            source_eos: dict[str, list[EO]],
    ) -> dict:
        """
        Собрать структуру источников для solver

        Результат:
        {
            "P101": {
                "eos": [
                    {
                        "material_id": "84597",
                        "batch":       "Z084597001",
                        "is_reserved": False,
                    },
                    ...
                ],
                "occupancy": 10,
                "free_space": 11,
            },
            ...
        }
        """
        sources = {}

        for cell in source_cells:
            eos = source_eos.get(cell.cell_id, [])
            sources[cell.cell_id] = {
                "eos": [
                    {
                        "material_id": eo.material_id,
                        "batch": eo.batch,
                        "is_reserved": eo.is_reserved,
                    }
                    for eo in eos
                ],
                "occupancy": cell.occupancy,
                "free_space": cell.free_space,
            }

        return sources

    def _build_warehouse(self, all_cells: list[Cell]) -> dict:
        """
        Собрать краткую структуру всего склада для solver

        Пустая ячейка  → material_id=None, batch=None
        Непустая ячейка → material_id и batch из первого ЕО

        Результат:
        {
            "P101": {
                "material_id": "84597",
                "batch":       "Z084597001",
                "occupancy":   10,
                "free_space":  11,
            },
            "P115": {
                "material_id": None,
                "batch":       None,
                "occupancy":   0,
                "free_space":  21,
            },
            ...
        }
        """
        warehouse = {}

        for cell in all_cells:
            first_eo = cell.eo_list[0] if cell.eo_list else None
            warehouse[cell.cell_id] = {
                "material_id": first_eo.material_id if first_eo else None,
                "batch": first_eo.batch if first_eo else None,
                "occupancy": cell.occupancy,
                "free_space": cell.free_space,
            }

        return warehouse
