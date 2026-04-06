"""
generator_2.py - сценарий 2

Диапазон для освобождения: P200 - P220 (ряд 2, блоки C и D)

Намеренно выгодный маршрут:
    Источник: P213 - 8 паллетов (минимум ЕО в диапазоне)
    Цель: P116 - 12 паллетов (свободно 9 мест, все 8 влезут)

Целевая ячейка P116 находится в ряду 1 (блок B) - за пределами диапазона
Алгоритм ищет цель по всему складу, не только внутри диапазона

Остальные ячейки заполнены на 40-80% разными продуктами -
чтобы P213 → P116 был явно оптимальным выбором алгоритма

Все необходимые функции определены в модуле generator_utils.py
"""
import json

from generator_utils import random, Cell, EO, PRODUCTS, _fill_cell, init_counter

random.seed(99)  # отдельный seed для воспроизводимости сценария 2

init_counter(7210000200000000)  # стартовый номер ЕО


def generate_scenario_2() -> tuple[list[Cell], list[EO]]:
    """
    Генерирует данные сценария 2.

    Возвращает:
        cells - список объектов Cell (P200-P220 + P116 как целевая)
        eos - список объектов EO (все паллеты)

    Ключевые ячейки:
        P213 - 8 паллетов (оптимальный источник, минимум в диапазоне)
        P116 - 12 паллетов (оптимальная цель, свободно 9 мест, все 8 влезут)

    Остальные ячейки диапазона P200-P220 - 40-80%, разные продукты.
    P116 намеренно выгоднее всех других возможных целей на складе
    """

    all_cells: list[Cell] = []
    all_eos: list[EO] = []

    key_product = PRODUCTS[1]  # СТЕЛ АРТ БУТ

    # P213: 8 паллетов - минимум в диапазоне → оптимальный источник
    cell_213, eos_213 = _fill_cell("P213", 8, key_product)
    all_cells.append(cell_213)
    all_eos.extend(eos_213)

    # P116: 12 паллетов → свободно 9 мест, все 8 из P213 влезут
    # Блок B (P111-P120) - сложность P213(D) → P116(B) = 1.25
    cell_116, eos_116 = _fill_cell("P116", 12, key_product)
    all_cells.append(cell_116)
    all_eos.extend(eos_116)

    # Диапазон P200-P220 (кроме P213)
    # Заполняем 40-80%, разные продукты

    skip = {"P213"}

    for num in range(200, 221):
        cell_id = f"P{num}"
        if cell_id in skip:
            continue

        # блок D почти полный — чтобы алгоритм не нашёл совместимую цель внутри диапазона
        if 211 <= num <= 220:
            count = random.randint(17, 20)
        else:
            count = random.randint(9, 17)   # блок C — 40-80%

        product = random.choice(PRODUCTS[2:])  # любой кроме key_product
        cell, eos = _fill_cell(cell_id, count, product)
        all_cells.append(cell)
        all_eos.extend(eos)

    # Ряд 1 P100-P120 (кроме P116)
    # Заполняем почти под завязку — чтобы P116 была явно лучшей целью
    for num in range(100, 121):
        cell_id = f"P{num}"
        if cell_id == "P116":
            continue

        count = random.randint(17, 20)  # 80-95% - мало свободного места
        product = random.choice(PRODUCTS)
        cell, eos = _fill_cell(cell_id, count, product)
        all_cells.append(cell)
        all_eos.extend(eos)

    return all_cells, all_eos


def export_to_json(cells: list[Cell], eos: list[EO], path: str = "scenario_2.json") -> None:
    """Сохранить сгенерированные данные в JSON-файл."""
    data = {
        "scenario": 2,
        "description": "Оптимальный маршрут: P213 (8 ЕО) → P116 (свободно 9 мест, блок B)",
        "cells": [c.to_dict() for c in cells],
        "eos": [e.to_dict() for e in eos],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Экспорт: {path} ({len(cells)} ячеек, {len(eos)} ЕО)")


if __name__ == "__main__":
    print("\n  Генератор сценария 2")
    print("  " + "-" * 40)

    cells, eos = generate_scenario_2()

    print(f"  Ячеек сгенерировано : {len(cells)}")
    print(f"  ЕО сгенерировано    : {len(eos)}")
    print()

    # Ключевые ячейки
    key_ids = {"P213", "P116"}
    print("  Ключевые ячейки:")
    for cell in sorted(cells, key=lambda c: c.cell_id):
        if cell.cell_id in key_ids:
            label = "ИСТОЧНИК" if cell.cell_id == "P213" else "ЦЕЛЬ"
            print(f"    {cell.cell_id}: {cell.occupancy}/{cell.capacity} паллетов  ← {label}")

    print()
    print("  Диапазон P200-P220 (освобождаем):")
    range_200 = [c for c in cells if 200 <= int(c.cell_id[1:]) <= 220]
    for cell in sorted(range_200, key=lambda c: c.cell_id):
        bar = "█" * cell.occupancy + "░" * cell.free_space
        marker = " ← ИСТОЧНИК" if cell.cell_id == "P213" else ""
        print(f"    {cell.cell_id}: [{bar}] {cell.occupancy:>2}/{cell.capacity}{marker}")

    print()
    print("  Целевая зона P100-P120 (куда везём):")
    range_100 = [c for c in cells if 100 <= int(c.cell_id[1:]) <= 120]
    for cell in sorted(range_100, key=lambda c: c.cell_id):
        bar = "█" * cell.occupancy + "░" * cell.free_space # :)
        marker = " ← ЦЕЛЬ" if cell.cell_id == "P116" else ""
        print(f"    {cell.cell_id}: [{bar}] {cell.occupancy:>2}/{cell.capacity}{marker}")

    print()
    export_to_json(cells, eos)