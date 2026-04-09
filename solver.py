"""
solver.py — поиск оптимальной ячейки для освобождения

Получает от blender:
    - sources:   dict — ячейки диапазона с ЕО
    - warehouse: dict — весь склад

Алгоритм:
    1. Для каждой ячейки диапазона ищет лучшую целевую ячейку
    2. Из всех пар выбирает с минимальными очками сложности
    3. Если для ячейки нет подходящей цели — пропускает её

Возвращает:
    RouteResult с результатом или error если решения нет

Использование:
    from solver import Solver
    solver = Solver()
    result = solver.solve(sources, warehouse)
"""

from dataclasses import dataclass
from models import ComplexityMatrix


@dataclass
class RouteResult:
    """
    Результат работы solver.

    Использование:
        result = solver.solve(sources, warehouse)
        if result.success:
            print(result.source)   # "P101"
            print(result.target)   # "P108"
            print(result.eo_count) # 10
            print(result.score)    # 4.0
        else:
            print(result.error)
    """
    source:   str
    target:   str
    eo_count: int
    score:    float
    success:  bool = True
    error:    str  = ""


class Solver:

    def __init__(self) -> None:
        self._matrix = ComplexityMatrix()

    def solve(self, sources: dict, warehouse: dict) -> RouteResult:
        """
        Найти оптимальную пару источник → цель.

        Использование:
            solver = Solver()
            result = solver.solve(sources, warehouse)
            # result.success = True  → нашли
            # result.success = False → решения нет
        """
        best: RouteResult | None = None

        for source_id, source_data in sources.items():
            result = self._find_best_target(source_id, source_data, warehouse)
            if result is None:
                continue

            if best is None or result.score < best.score:
                best = result

        if best is None:
            return RouteResult(
                source="",
                target="",
                eo_count=0,
                score=0.0,
                success=False,
                error="Не найдено подходящих целевых ячеек. "
                      "Нет ячеек с достаточным свободным местом и совместимым продуктом.",
            )

        return best

    def _find_best_target(
        self,
        source_id: str,
        source_data: dict,
        warehouse: dict,
    ) -> RouteResult | None:
        """
        Найти лучшую целевую ячейку для одного источника.

        Возвращает RouteResult или None если подходящих целей нет.
        """
        eo_count = source_data["occupancy"]
        source_eos = source_data["eos"]

        if not source_eos:
            return None

        material_id = source_eos[0]["material_id"]
        batch        = source_eos[0]["batch"]

        best: RouteResult | None = None

        for target_id, target_data in warehouse.items():

            # не перемещаем в ту же ячейку
            if target_id == source_id:
                continue

            # мест должно хватить
            if target_data["free_space"] < eo_count:
                continue

            # непустая ячейка — проверяем совместимость material_id и batch
            if target_data["material_id"] is not None:
                if (target_data["material_id"] != material_id or
                        target_data["batch"] != batch):
                    continue

            # считаем очки
            score = self._matrix.calculate_score(source_id, target_id, eo_count)

            # ячейка вне матрицы — пропускаем
            if score < 0:
                continue

            if best is None or score < best.score:
                best = RouteResult(
                    source=source_id,
                    target=target_id,
                    eo_count=eo_count,
                    score=score,
                )

        return best