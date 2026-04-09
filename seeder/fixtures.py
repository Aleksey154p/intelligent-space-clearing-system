"""
fixtures.py - тестовые данные для наполнения виртуального склада

Используется только seeder.py
Не содержит никакой логики - только константы
"""

# Ячейки склада
CELLS: list[dict] = [
    # Блок A: P100 - P110
    {"cell_id": "P100", "capacity": 21, "is_blocked": 0},
    {"cell_id": "P101", "capacity": 21, "is_blocked": 0},
    {"cell_id": "P102", "capacity": 21, "is_blocked": 0},
    {"cell_id": "P103", "capacity": 21, "is_blocked": 0},
    {"cell_id": "P104", "capacity": 21, "is_blocked": 0},
    {"cell_id": "P105", "capacity": 21, "is_blocked": 0},
    {"cell_id": "P106", "capacity": 21, "is_blocked": 0},
    {"cell_id": "P107", "capacity": 21, "is_blocked": 0},
    {"cell_id": "P108", "capacity": 21, "is_blocked": 0},
    {"cell_id": "P109", "capacity": 21, "is_blocked": 0},
    {"cell_id": "P110", "capacity": 21, "is_blocked": 0},
    # Блок B: P111 - P120
    {"cell_id": "P111", "capacity": 21, "is_blocked": 0},
    {"cell_id": "P112", "capacity": 21, "is_blocked": 0},
    {"cell_id": "P113", "capacity": 21, "is_blocked": 0},
    {"cell_id": "P114", "capacity": 21, "is_blocked": 0},
    {"cell_id": "P115", "capacity": 21, "is_blocked": 0},
    {"cell_id": "P116", "capacity": 21, "is_blocked": 0},
    {"cell_id": "P117", "capacity": 21, "is_blocked": 0},
    {"cell_id": "P118", "capacity": 21, "is_blocked": 0},
    {"cell_id": "P119", "capacity": 21, "is_blocked": 0},
    {"cell_id": "P120", "capacity": 21, "is_blocked": 0},
    # Блок C: P200 - P210
    # {"cell_id": "P200", "capacity": 21, "is_blocked": 0},
    # {"cell_id": "P201", "capacity": 21, "is_blocked": 0},
    # {"cell_id": "P202", "capacity": 21, "is_blocked": 0},
    # {"cell_id": "P203", "capacity": 21, "is_blocked": 0},
    # {"cell_id": "P204", "capacity": 21, "is_blocked": 0},
    # {"cell_id": "P205", "capacity": 21, "is_blocked": 0},
    # {"cell_id": "P206", "capacity": 21, "is_blocked": 0},
    # {"cell_id": "P207", "capacity": 21, "is_blocked": 0},
    # {"cell_id": "P208", "capacity": 21, "is_blocked": 0},
    # {"cell_id": "P209", "capacity": 21, "is_blocked": 0},
    # {"cell_id": "P210", "capacity": 21, "is_blocked": 0},
    # # Блок D: P211 - P220
    # {"cell_id": "P211", "capacity": 21, "is_blocked": 0},
    # {"cell_id": "P212", "capacity": 21, "is_blocked": 0},
    # {"cell_id": "P213", "capacity": 21, "is_blocked": 0},
    # {"cell_id": "P214", "capacity": 21, "is_blocked": 0},
    # {"cell_id": "P215", "capacity": 21, "is_blocked": 0},
    # {"cell_id": "P216", "capacity": 21, "is_blocked": 0},
    # {"cell_id": "P217", "capacity": 21, "is_blocked": 0},
    # {"cell_id": "P218", "capacity": 21, "is_blocked": 0},
    # {"cell_id": "P219", "capacity": 21, "is_blocked": 0},
    # {"cell_id": "P220", "capacity": 21, "is_blocked": 0},
]

# Виртуальный ассортимент
PRODUCTS: list[dict] = [
    {"product": "EFES PILSENER БУТ 20 0,5Л КОР ЕВРО SL RU", "material_id": "10011", "batch": "Z010011001",
     "production_date": "01/03/26", "quantity": 45, "weight_kg": 520.0},
    {"product": "СТЕЛ АРТ БУТ 20 0,44Л КОР ЕВРО SL RU", "material_id": "84597", "batch": "Z084597001",
     "production_date": "05/03/26", "quantity": 40, "weight_kg": 597.0},
    {"product": "БЕЛЫЙ МЕДВЕДЬ БАН 24 0,45Л БЛ ЕВРО SL RU", "material_id": "20033", "batch": "Z020033001",
     "production_date": "09/03/26", "quantity": 72, "weight_kg": 610.0},
    {"product": "СОКОЛ ПЭТ 6 1,5Л ТЕР ЕВРО SL RU", "material_id": "30044", "batch": "Z030044001",
     "production_date": "12/03/26", "quantity": 48, "weight_kg": 480.0},
    {"product": "HOEGAARDEN БУТ 24 0,33Л КОР ЕВРО SL RU", "material_id": "40055", "batch": "Z040055001",
     "production_date": "18/03/26", "quantity": 45, "weight_kg": 540.0},
    {"product": "BUD БАН 24 0,5Л БЛ ЕВРО SL RU", "material_id": "50066", "batch": "Z050066001",
     "production_date": "22/03/26", "quantity": 72, "weight_kg": 625.0},
    {"product": "CORONA БУТ 24 0,33Л КОР ЕВРО SL RU", "material_id": "60077", "batch": "Z060077001",
     "production_date": "26/03/26", "quantity": 45, "weight_kg": 510.0},
]
