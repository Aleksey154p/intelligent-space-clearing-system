"""
eo.py — модель паллета (единица обработки)

Данные приходят из SAP в виде JSON:
{
    "eo_id":           "7210000126042964",
    "product":         "СТЕЛ АРТ БУТ 20 0,44Л КОР ЕВРО SL RU",
    "material_id":     "84597",
    "quantity":        40,
    "batch":           "Z030969201",
    "production_date": "09/03/26",
    "weight_kg":       597,
    "cell_id":         "P105",
    "is_reserved":     False,
    "reservation_id":  None
}
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class EO:
    eo_id: str
    product: str
    material_id: str
    quantity: int
    batch: str
    production_date: str  # формат "DD/MM/YY"
    weight_kg: float
    cell_id: str  # текущая ячейка
    is_reserved: bool = False
    reservation_id: Optional[str] = None  # например "DA07, R01"

    def __str__(self) -> str:
        reserved = f" [РЕЗЕРВ: {self.reservation_id}]" if self.is_reserved else ""
        return (
            f"EO {self.eo_id} | {self.product} | "
            f"{self.quantity} шт | {self.production_date} | "
            f"ячейка: {self.cell_id}{reserved}"
        )
