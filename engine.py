"""
engine.py — оркестратор системы

Управляет порядком вызовов модулей:
    cli → supervisor → blender → solver → cli

Использование:
    python engine.py
"""

from cli import (
    show_welcome,
    get_range_choice,
    show_invalid_choice,
    show_row2_disabled,
    show_analyzing,
    show_result,
    ask_continue,
    show_goodbye,
)
from supervisor import Supervisor
from blender import Blender
from solver import Solver
from seeder.seeder import run as seed_run
from warehouse_view import draw_warehouse

import time

# диапазоны, соответствующие пунктам меню
RANGES = {
    "1": ("P100", "P120"),
    "2": ("P200", "P220"),
}


def run() -> None:
    supervisor = Supervisor()
    blender = Blender()
    solver = Solver()

    show_welcome()

    while True:
        choice = get_range_choice()

        if choice == "0":
            show_goodbye()
            break

        if choice == "3":
            seed_run()
            print("Новый склад создан.")
            continue

        if choice == "4":
            draw_warehouse()
            continue

        if choice == "2":
            show_row2_disabled()
            continue

        if choice not in RANGES:
            show_invalid_choice()
            continue

        start, end = RANGES[choice]

        show_analyzing()

        start_time = time.perf_counter()
        # пайплайн
        source_cells = supervisor.get_source_cells(start, end)
        source_eos = supervisor.get_source_eos(source_cells)
        all_cells = supervisor.get_all_cells()
        sources, warehouse = blender.prepare(source_cells, source_eos, all_cells)
        result = solver.solve(sources, warehouse)

        show_result(result)

        result_time = time.perf_counter() - start_time
        print(f"  Время за которое алгоритм выполнил работу: {result_time:.2f} секунд")

        if not ask_continue():
            show_goodbye()
            break


if __name__ == "__main__":
    run()
