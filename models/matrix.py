"""
matrix.py — матрица сложности маршрутов между блоками склада
Фактически это два ряда, Р100-Р120, P200-P220
Разделение на блоки A, B, C, D, реализовано для внутренней логики вариативной сложности
Блоки склада (MVP — 1 ряд, 4 блока):
A = P100-110, B = P111-120, C = P200-210, D = P211-220

Значения сложности:
Внутри A: 0.4
Внутри B: 0.4 - симметрично A
Внутри C: 0.4 - симметрично A
Внутри D: 0.4 - симметрично A

A ↔ B: 0.8 - соседи по горизонтали, ряд 1
C ↔ D: 0.8 - соседи по горизонтали, ряд 2

A ↔ C: 1.25 - прямо вниз
B ↔ D: 1.25 - прямо вниз

A ↔ D: 1.85 - наискосок
B ↔ C: 1.85 - наискосок

Для наглядности см. фото part_3, будут прикреплены к идее
"""

"""
Строки 31 - 52 захаркодены, для удобства реализации mvp
В дальнейшем планируется заменить на динамическое изменение
"""

BLOCK_RANGES: dict[str, tuple[int, int]] = {
    "A": (100, 110),
    "B": (111, 120),
    "C": (200, 210),
    "D": (211, 220),
}

COMPLEXITY_TABLE: dict[tuple[str, str], float] = {
    ("A", "A"): 0.4,
    ("B", "B"): 0.4,
    ("C", "C"): 0.4,
    ("D", "D"): 0.4,

    ("A", "B"): 0.8, ("B", "A"): 0.8,
    ("C", "D"): 0.8, ("D", "C"): 0.8,

    ("A", "C"): 1.25, ("C", "A"): 1.25,
    ("B", "D"): 1.25, ("D", "B"): 1.25,

    ("A", "D"): 1.85, ("D", "A"): 1.85,
    ("B", "C"): 1.85, ("C", "B"): 1.85,
}


def get_block(cell_id: str) -> str | None:
    """
    Определить блок по идентификатору ячейки.

    get_block("P105") → "A"
    get_block("P115") → "B"
    get_block("P999") → None
    """
    try:
        number = int(cell_id.lstrip("P"))
    except ValueError:
        return None

    for block, (start, end) in BLOCK_RANGES.items():
        if start <= number <= end:
            return block

    return None


class ComplexityMatrix:
    """
    Матрица сложности маршрутов

    Сейчас работает на захардкоденных константах
    В будущем: BLOCK_RANGES и COMPLEXITY_TABLE грузятся из БД,
    меняются через UI без разработчика

    Использование:
        matrix = ComplexityMatrix()
        score = matrix.get_complexity("P105", "P215") → 1.85
        total = matrix.calculate_score("P105", "P215", 6) → 11.1
    """

    def get_complexity(self, from_cell: str, to_cell: str) -> float:
        """
        Коэффициент сложности между двумя ячейками
        Возвращает -1.0 если ячейка не принадлежит ни одному блоку

        Использование:
            matrix = ComplexityMatrix()
            matrix.get_complexity("P105", "P215") → 1.85
            matrix.get_complexity("P105", "P108") → 0.4
        """
        from_block = get_block(from_cell)
        to_block = get_block(to_cell)

        if from_block is None or to_block is None:
            return -1.0

        return COMPLEXITY_TABLE.get((from_block, to_block), -1.0)

    def calculate_score(self, from_cell: str, to_cell: str, eo_count: int) -> float:
        """
        Очки сложности для перемещения eo_count паллетов.

        Формула: коэффициент * количество ЕО
        Пример: P105 → P215, 6 ЕО → 1.85 * 6 = 11.1

        Использование:
            matrix = ComplexityMatrix()
            matrix.calculate_score("P105", "P215", 6) → 11.1
            matrix.calculate_score("P105", "P108", 10) → 4.0
        """
        complexity = self.get_complexity(from_cell, to_cell)
        if complexity < 0:
            return -1.0
        return round(complexity * eo_count, 2)