import random
from models.eo import EO
from models.cell import Cell

# Виртуальный ассортимент, которым буду наполнять ячейки
PRODUCTS = [
    {"product": "EFES PILSENER БУТ 20 0,5Л КОР ЕВРО SL RU", "material_id": "10011", "quantity": 45, "weight_kg": 520},
    {"product": "СТЕЛ АРТ БУТ 20 0,44Л КОР ЕВРО SL RU", "material_id": "84597", "quantity": 40, "weight_kg": 597},
    {"product": "БЕЛЫЙ МЕДВЕДЬ БАН 24 0,45Л БЛ ЕВРО SL RU", "material_id": "20033", "quantity": 72, "weight_kg": 610},
    {"product": "СОКОЛ ПЭТ 6 1,5Л ТЕР ЕВРО SL RU", "material_id": "30044", "quantity": 48, "weight_kg": 480},
    {"product": "HOEGAARDEN БУТ 24 0,33Л КОР ЕВРО SL RU", "material_id": "40055", "quantity": 45, "weight_kg": 540},
    {"product": "BUD БАН 24 0,5Л БЛ ЕВРО SL RU", "material_id": "50066", "quantity": 72, "weight_kg": 625},
    {"product": "CORONA БУТ 24 0,33Л КОР ЕВРО SL RU", "material_id": "60077", "quantity": 45, "weight_kg": 510},
]

# Даты для виртуальной продукции
DATES = [
    "01/03/26", "05/03/26", "09/03/26",
    "12/03/26", "18/03/26", "22/03/26",
]

_eo_counter = 0

def _next_eo_id() -> str:
    global _eo_counter
    _eo_counter += 1
    return str(_eo_counter)

def init_counter(start: int) -> None:
    """Установить стартовый номер ЕО перед началом генерации сценария"""
    global _eo_counter
    _eo_counter = start

def _next_batch(date: str) -> str:
    """
    Генерация номера партии в формате SAP: Z + DDMM + XXXXX
    12/03/26
    """
    day, month, _ = date.split("/")
    tail = str(random.randint(10000, 99999))
    return f"Z{day}{month}{tail}"


def _make_eo(cell_id: str, product_data: dict, date: str,
             is_reserved: bool = False, reservation_id: str = None) -> EO:
    """Создать объект EO"""
    batch = _next_batch(date)
    day, month, year = date.split("/")
    exp_year = str(int(year) + 1)
    expiry = f"{day}/{month}/{exp_year}"

    return EO(
        eo_id=_next_eo_id(),
        product=product_data["product"],
        material_id=product_data["material_id"],
        quantity=product_data["quantity"],
        batch=batch,
        production_date=date,
        expiry_date=expiry,
        weight_kg=product_data["weight_kg"],
        cell_id=cell_id,
        is_reserved=is_reserved,
        reservation_id=reservation_id,
    )


def _fill_cell(cell_id: str, count: int, product_data: dict = None) -> tuple[Cell, list[EO]]:
    """
    Создать ячейку с заданным количеством ЕО.
    Если product_data не передан — берём случайный продукт.
    """
    p = product_data if product_data else random.choice(PRODUCTS)  # один продукт на всю ячейку
    eos = []
    for _ in range(count):
        d = random.choice(DATES)
        eo = _make_eo(cell_id, p, d)
        eos.append(eo)

    cell = Cell(
        cell_id=cell_id,
        capacity=21,
        eo_list=[eo.eo_id for eo in eos],
        is_blocked=False,
    )
    return cell, eos