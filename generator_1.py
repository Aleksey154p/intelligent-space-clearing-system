"""
generator_1.py - сценарий 1

Диапазон для освобождения: P100 - P120 (ряд 1, блоки A и B)

Намеренно выгодный маршрут:
    Источник: P105 - 5 паллетов (минимум ЕО в диапазоне)
    Цель: P108 - 11 паллетов (свободно 10 мест, все 5 влезут)

Остальные ячейки заполнены на 40–80% разными продуктами -
чтобы P105 → P108 был явно оптимальным выбором алгоритма

Все необходимые функции определены в модуле generator_utils.py
"""
import json

from generator_utils import random, Cell, EO, PRODUCTS, _fill_cell, init_counter

random.seed(42)  # фиксирую seed - данные воспроизводимы при каждом запуске

init_counter(7210000100000000)  # стартовый номер ЕО


def generate_scenario_1() -> tuple[list[Cell], list[EO]]:
    """
    Генерирует данные сценария 1.

    Возвращает:
        cells - список объектов Cell (P100 - P120)
        eos - список объектов EO (все паллеты)

    Ключевые ячейки:
        P105 - 5 паллетов одного продукта (оптимальный источник)
        P108 - 11 паллетов одного продукта (оптимальная цель, свободно 10 мест)

    Остальные ячейки — 40–80% заполненности, разные продукты.
    """

    all_cells: list[Cell] = []
    all_eos: list[EO] = []

    # Фиксированный продукт для P105 и P108 - одинаковый,
    # чтобы перемещение было логичным (один продукт в одну ячейку)
    key_product = PRODUCTS[0]  # EFES PILSENER

    # Ключевые ячейки

    # P105: 5 паллетов - минимум в диапазоне → оптимальный источник
    cell_105, eos_105 = _fill_cell("P105", 5, key_product)
    all_cells.append(cell_105)
    all_eos.extend(eos_105)

    # P108: 11 паллетов → свободно 10 мест, все 5 из P105 влезут
    cell_108, eos_108 = _fill_cell("P108", 11, key_product)
    all_cells.append(cell_108)
    all_eos.extend(eos_108)

    # Остальные ячейки P100 - P120
    # Заполняем 40–80% (от 21 места = 9–17 паллетов)
    # P105 и P108 уже созданы — пропускаем

    skip = {"P105", "P108"}

    for num in range(100, 121):
        cell_id = f"P{num}"
        if cell_id in skip:
            continue

        count = random.randint(9, 17)  # 40–80% от 21
        product = random.choice(PRODUCTS[1:])  # любой кроме key_product
        cell, eos = _fill_cell(cell_id, count, product)
        all_cells.append(cell)
        all_eos.extend(eos)

    return all_cells, all_eos


def export_to_json(cells: list[Cell], eos: list[EO], path: str = "scenario_1.json") -> None:
    """Сохранить сгенерированные данные в JSON-файл."""
    data = {
        "scenario": 1,
        "description": "Оптимальный маршрут: P105 (5 ЕО) → P108 (свободно 10 мест)",
        "cells": [c.to_dict() for c in cells],
        "eos": [e.to_dict() for e in eos],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Экспорт: {path} ({len(cells)} ячеек, {len(eos)} ЕО)")


if __name__ == "__main__":
    print("\n  Сценарий 1")
    print("  " + "-" * 40)

    cells, eos = generate_scenario_1()

    print(f"  Ячеек сгенерировано : {len(cells)}")
    print(f"  ЕО сгенерировано    : {len(eos)}")
    print()

    # Показываю ключевые ячейки
    key_ids = {"P105", "P108"}
    print("  Ключевые ячейки:")
    for cell in sorted(cells, key=lambda c: c.cell_id):
        if cell.cell_id in key_ids:
            print(
                f"    {cell.cell_id}: {cell.occupancy}/{cell.capacity} паллетов  ← {'ИСТОЧНИК' if cell.cell_id == 'P105' else 'ЦЕЛЬ'}")

    print()
    print("  Все ячейки диапазона P100 - P120:")
    for cell in sorted(cells, key=lambda c: c.cell_id):
        bar = "█" * cell.occupancy + "░" * cell.free_space  # :)
        marker = " ← ИСТОЧНИК" if cell.cell_id == "P105" else (" ← ЦЕЛЬ" if cell.cell_id == "P108" else "")
        print(f"    {cell.cell_id}: {bar} {cell.occupancy:>2}/{cell.capacity}{marker}")

    print()
    export_to_json(cells, eos)
