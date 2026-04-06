"""
algorithm.py - логика выбора оптимальной ячейки и построения маршрута

Алгоритм работает с двумя рядами, четырьмя блоками (A, B, C, D)
Масштабирование - отдельная задача

Вход:
    - диапазон ячеек для освобождения (например P200 - P220)
    - все ячейки склада
    - все ЕО склада

Выход:
    - RouteResult - оптимальная ячейка-источник, цель, маршрут, очки
"""

from dataclasses import dataclass, field
from models.cell import Cell
from models.eo import EO
from models.matrix import ComplexityMatrix


#  Структуры результата

@dataclass
class RouteStep:
    """Один шаг маршрута"""
    step_num: int
    from_cell: str
    to_cell: str
    eo_count: int
    complexity: float
    score: float

    def __str__(self) -> str:
        return (
            f"  Шаг {self.step_num}: {self.eo_count} ЕО "
            f"из {self.from_cell} → {self.to_cell} "
            f"— {self.score} очков сложности"
            f"\n  Далее планируется модифицировать до разбития операции на шаги"
        )


@dataclass
class RouteResult:
    """Результат работы алгоритма"""
    source_cell: str  # ячейка, которую освобождаю
    target_cell: str  # ячейка куда везу
    total_score: float  # суммарные очки сложности
    steps: list[RouteStep] = field(default_factory=list)
    success: bool = True
    error: str = ""  # причина если success=False

    def __str__(self) -> str:
        if not self.success:
            return f"  Ошибка: {self.error}"

        lines = [
            f"\n  Оптимальная ячейка для освобождения  : {self.source_cell}",
            f"  Ячейка будет доставляться продукцией : {self.target_cell}",
            f"  Итого очков сложности : {self.total_score}",
            f"  {'-' * 5}",
        ]
        for step in self.steps:
            lines.append(str(step))
        lines.append(f"  {'-' * 5}")
        lines.append("  Сфотографируйте и выполните через режим 2.2 - 3030")
        return "\n".join(lines)


#  Вспомогательные функции

def _parse_range(range_str: str) -> tuple[int, int]:
    """
    Распарсить строку диапазона в два числа

    Примеры:
        "P100-P120" → (100, 120)
        "P200-P220" → (200, 220)
    """
    parts = range_str.upper().replace(" ", "").split("-")
    start = int(parts[0].lstrip("P"))
    end = int(parts[1].lstrip("P"))
    return start, end


def _cells_in_range(
        cells: dict[str, Cell],
        start: int,
        end: int,
) -> list[Cell]:
    """
    Получить непустые незаблокированные ячейки из диапазона
    Только те у которых есть ЕО для перемещения
    """
    result = []
    for cell_id, cell in cells.items():
        try:
            num = int(cell_id.lstrip("P"))
        except ValueError:
            continue
        if start <= num <= end and not cell.is_blocked and cell.occupancy > 0:
            result.append(cell)
    return result


def _find_best_target(
        source: Cell,
        cells: dict[str, Cell],
        eos: dict[str, EO],
        matrix: ComplexityMatrix,
) -> tuple[Cell | None, float]:
    """
    Найти лучшую целевую ячейку для источника

    Правила:
        - не сам источник
        - не заблокирована
        - влезают все ЕО источника (free_space >= occupancy источника)
        - продукт совпадает с продуктом источника (или ячейка пустая)
        - минимальная сложность маршрута

    Возвращает:
        (лучшая ячейка, очки) или (None, -1) если цель не найдена
    """
    best_cell: Cell | None = None
    best_score: float = float("inf")

    eo_count = source.occupancy

    # определяем продукт источника
    source_material = eos[source.eo_list[0]].material_id

    for cell_id, cell in cells.items():
        # пропускаем сам источник
        if cell_id == source.cell_id:
            continue

        # пропускаем заблокированные
        if cell.is_blocked:
            continue

        # пропускаем если не влезут все ЕО
        if cell.free_space < eo_count:
            continue

        # проверяем совместимость продукта
        # пустая ячейка подходит всегда, непустая - только если тот же продукт
        if cell.occupancy > 0:
            target_material = eos[cell.eo_list[0]].material_id
            if target_material != source_material:
                continue

        # считаем очки
        score = matrix.calculate_score(source.cell_id, cell_id, eo_count)
        if score < 0:
            continue

        if score < best_score:
            best_score = score
            best_cell = cell

    if best_cell is None:
        return None, -1.0

    return best_cell, best_score


#  Основная функция


def find_optimal_route(
        range_str: str,
        cells: dict[str, Cell],
        eos: dict[str, EO],
) -> RouteResult:
    """
    Найти оптимальный маршрут для освобождения ячейки в диапазоне

    Аргументы:
        range_str    - диапазон ячеек, например "P100-P120"
        cells        - все ячейки склада {cell_id: Cell}
        eos          - все ЕО склада {eo_id: EO}
        min_fill_pct - минимальная заполненность цели после размещения (защита от фрагментации)

    Возвращает:
        RouteResult с оптимальным маршрутом или ошибкой
    """
    matrix = ComplexityMatrix()

    # Шаг 1 - парсим диапазон
    try:
        range_start, range_end = _parse_range(range_str)
    except Exception:
        return RouteResult(
            source_cell="", target_cell="",
            total_score=0, success=False,
            error=f"Неверный формат диапазона: '{range_str}'. Ожидается 'P100-P120'",
        )

    # Шаг 2 - получаем кандидатов из диапазона
    candidates = _cells_in_range(cells, range_start, range_end)

    if not candidates:
        return RouteResult(
            source_cell="", target_cell="",
            total_score=0, success=False,
            error=f"В диапазоне {range_str} нет доступных ячеек для освобождения",
        )

    # Шаг 3 - для каждого кандидата ищем лучшую цель и считаем очки
    best_source: Cell | None = None
    best_target: Cell | None = None
    best_score: float = float("inf")

    for source in candidates:
        target, score = _find_best_target(source, cells, eos, matrix)
        if target is None:
            continue

        if score < best_score:
            best_score = score
            best_source = source
            best_target = target

    # Шаг 4 - проверяю, что нашли маршрут
    if best_source is None or best_target is None:
        return RouteResult(
            source_cell="", target_cell="",
            total_score=0, success=False,
            error="Не удалось найти подходящую целевую ячейку. "
                  "Нет ячеек с достаточным свободным местом вне диапазона.",
        )

    # Шаг 5 - строим пошаговый маршрут
    eo_count = best_source.occupancy
    complexity = matrix.get_complexity(best_source.cell_id, best_target.cell_id)

    step = RouteStep(
        step_num=1,
        from_cell=best_source.cell_id,
        to_cell=best_target.cell_id,
        eo_count=eo_count,
        complexity=complexity,
        score=best_score,
    )

    return RouteResult(
        source_cell=best_source.cell_id,
        target_cell=best_target.cell_id,
        total_score=best_score,
        steps=[step],
        success=True,
    )
