"""
warehouse_view.py — визуальная проверка состояния склада

Запускается отдельно от основной программы
Показывает все ячейки склада с заполненностью и продуктом

Использование:
    python warehouse_view.py
"""

from repository import Repository

WIDTH = 62


def _bar(occupancy: int, capacity: int) -> str:
    filled = "█" * occupancy
    empty  = "░" * (capacity - occupancy)
    return f"[{filled}{empty}]"


def _short_product(product: str) -> str:
    return product[:28] if len(product) > 28 else product


def _divider() -> str:
    return "+" + "-" * (WIDTH - 2) + "+"


def _row(content: str) -> str:
    inner = WIDTH - 4
    return f"| {content.ljust(inner)} |"


def draw_warehouse() -> None:
    repo = Repository()
    cells = repo.get_all_cells()
    cells.sort(key=lambda c: c.cell_id)

    print()
    print(_divider())
    print(_row(f"  ВИРТУАЛЬНЫЙ СКЛАД  |  Ячеек: {len(cells)}"))
    print(_divider())

    for cell in cells:
        first_eo = cell.eo_list[0] if cell.eo_list else None
        product  = _short_product(first_eo.product) if first_eo else "— пусто —"
        batch    = first_eo.batch if first_eo else "—"
        status   = "  [ЗАБЛОК]" if cell.is_blocked else ""

        bar  = _bar(cell.occupancy, cell.capacity)
        fill = f"{cell.occupancy:>2}/{cell.capacity}"

        print(_row(""))
        print(_row(f"  {cell.cell_id}  {bar}  {fill}{status}"))
        print(_row(f"      {product}"))
        print(_row(f"      {batch}"))

    print(_row(""))
    print(_divider())
    print()


if __name__ == "__main__":
    draw_warehouse()