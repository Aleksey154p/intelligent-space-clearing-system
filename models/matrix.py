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

from typing import Optional

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


def get_block(cell_id: str) -> Optional[str]:
    """
    Определить блок (A/B/C/D) по идентификатору ячейки

    Примеры:
        get_block("P105") → "A"
        get_block("P115") → "B"
        get_block("P205") → "C"
        get_block("P215") → "D"
        get_block("P999") → None  # Блок не обнаружен
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
    Матрица сложности маршрутов между блоками склада

    Использование:
        matrix = ComplexityMatrix()
        score = matrix.get_complexity("P105", "P215") # → 1.85
        total_score = matrix.calculate_score("P105", "P215", 6) # → 11.1
    """

    def get_complexity(self, from_cell: str, to_cell: str) -> float:
        """
        Получить коэффициент сложности между двумя ячейками
        Возвращает -1.0 если один из блоков неизвестен
        """
        from_block = get_block(from_cell)
        to_block = get_block(to_cell)

        if from_block is None or to_block is None:
            return -1.0

        return COMPLEXITY_TABLE.get((from_block, to_block), -1.0)

    def calculate_score(self, from_cell: str, to_cell: str, eo_count: int) -> float:
        """
        Рассчитать очки сложности для перемещения

        Формула: сложность * количество ЕО = очки

        Пример:
            P105 → P215, 6 ЕО
            блок A → блок D = 1.85
            1.85 * 6 = 11.1 очков
        """
        complexity = self.get_complexity(from_cell, to_cell)
        if complexity < 0:
            return -1.0
        return round(complexity * eo_count, 2)

    def show_table(self) -> None:
        """Вывести матрицу сложности в терминал"""
        blocks = ["A", "B", "C", "D"]
        col_w = 8

        print("\n  Матрица сложности маршрутов")
        print("  " + "─" * (col_w * 5))

        header = f"{'':>{col_w}}" + "".join(f"{b:>{col_w}}" for b in blocks)
        print(header)

        for from_b in blocks:
            row = f"{from_b:>{col_w}}"
            for to_b in blocks:
                val = COMPLEXITY_TABLE.get((from_b, to_b), 0.0)
                row += f"{val:>{col_w}.2f}"
            print(row)

        print("  " + "─" * (col_w * 5))
        print()
        print("  Диапазоны блоков:")
        for block, (start, end) in BLOCK_RANGES.items():
            print(f"    Блок {block}: P{start} – P{end}")
        print()
