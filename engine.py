"""
engine.py — главная точка входа.

Управляет сессией:
    1. Показывает меню выбора сценария
    2. Загружает тестовые данные
    3. Запрашивает диапазон ячеек
    4. Запускает алгоритм
    5. Выводит результат
"""

from algorithm import find_optimal_route
from generator_1 import generate_scenario_1
from generator_2 import generate_scenario_2


#  Вспомогательный вывод


def _header() -> None:
    print("  MVP v0.1")


def _divider() -> None:
    print("-" * 5)


#  Загрузка сценария


def _load_scenario(choice: str) -> tuple[dict, dict, str] | None:
    """
    Загрузить тестовые данные выбранного сценария

    Возвращает:
        (cells, eos, default_range) или None если выбор неверный
    """
    if choice == "1":
        print("\n  Загрузка сценария 1 (P100–P120)")
        cells_list, eos_list = generate_scenario_1()
        default_range = "P100-P120"

    elif choice == "2":
        print("\n  Загрузка сценария 2 (P200–P220)")
        cells_list, eos_list = generate_scenario_2()
        default_range = "P200-P220"

    else:
        return None

    cells = {c.cell_id: c for c in cells_list}
    eos = {e.eo_id: e for e in eos_list}

    print(f"  Загружено: {len(cells)} ячеек, {len(eos)} ЕО")
    return cells, eos, default_range


#  Показ склада


def _show_warehouse(cells: dict, range_str: str) -> None:
    """Показать визуализацию ячеек диапазона"""
    try:
        parts = range_str.upper().replace(" ", "").split("-")
        start = int(parts[0].lstrip("P"))
        end = int(parts[1].lstrip("P"))
    except Exception:
        return

    print(f"\n  Ячейки диапазона {range_str}:")
    _divider()

    range_cells = [
        c for cid, c in cells.items()
        if start <= int(cid.lstrip("P")) <= end
    ]
    range_cells.sort(key=lambda c: c.cell_id)

    for cell in range_cells:
        """
        Для обработки заблокированных, зарезервированных и пр.ео
        функционал еще не готов
        """
        bar = "█" * cell.occupancy + "░" * cell.free_space
        status = "ЗАБЛОК" if cell.is_blocked else f"{cell.occupancy:>2}/{cell.capacity}"
        print(f"  {cell.cell_id}: [{bar}] {status}")

    _divider()


def main() -> None:
    _header()

    while True:
        # Выбор сценария
        print("\n  Выберите тестовый сценарий:")
        print("  [1] Сценарий 1 — диапазон P100–P120")
        print("  [2] Сценарий 2 — диапазон P200–P220")
        print("  [0] Выход")
        print()

        choice = input("  Ваш выбор: ").strip()

        if choice == "0":
            print("\n  До свидания. Я старался.\n")
            break

        result = _load_scenario(choice)
        if result is None:
            print("  Неверный выбор. Попробуйте снова.")
            continue

        cells, eos, default_range = result

        # Ввод диапазона
        print(f"\n  Диапазон по умолчанию: {default_range}")
        raw = input(f"  Введите диапазон = нажать Enter !функционал не доделан!: ").strip()
        range_str = raw if raw else default_range

        # Визуализация склада
        _show_warehouse(cells, range_str)

        # Запуск алгоритма
        print(f"\n  Анализ диапазона {range_str}")
        result = find_optimal_route(range_str, cells, eos)

        # Вывод результата
        print("\n" + "-" * 5)
        print("  РЕЗУЛЬТАТ АНАЛИЗА")
        print("-" * 5)
        print(result)
        print("-" * 5)

        # Продолжить?
        print("\n  [Enter] Новый анализ  [0] Выход")
        if input("  ").strip() == "0":
            print("\n  До свидания. Я старался.\n")
            break


if __name__ == "__main__":
    main()
