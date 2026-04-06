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
    "expiry_date":     "09/03/27",
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
    expiry_date: str  # формат "DD/MM/YY"
    weight_kg: float
    cell_id: str  # текущая ячейка
    is_reserved: bool = False
    reservation_id: Optional[str] = None  # например "DA07, R01"

    @classmethod
    def from_dict(cls, data: dict) -> "EO":
        """Создать EO из словаря (распарсенного JSON из SAP)"""
        return cls(
            eo_id=data["eo_id"],
            product=data["product"],
            material_id=data["material_id"],
            quantity=data["quantity"],
            batch=data["batch"],
            production_date=data["production_date"],
            expiry_date=data["expiry_date"],
            weight_kg=data["weight_kg"],
            cell_id=data["cell_id"],
            is_reserved=data.get("is_reserved", False),
            reservation_id=data.get("reservation_id", None),
        )

    def to_dict(self) -> dict:
        """Сериализовать EO обратно в словарь"""
        return {
            "eo_id": self.eo_id,
            "product": self.product,
            "material_id": self.material_id,
            "quantity": self.quantity,
            "batch": self.batch,
            "production_date": self.production_date,
            "expiry_date": self.expiry_date,
            "weight_kg": self.weight_kg,
            "cell_id": self.cell_id,
            "is_reserved": self.is_reserved,
            "reservation_id": self.reservation_id,
        }

    def __str__(self) -> str:
        reserved = f" [РЕЗЕРВ: {self.reservation_id}]" if self.is_reserved else ""
        return (
            f"EO {self.eo_id} | {self.product} | "
            f"{self.quantity} шт | {self.production_date} | "
            f"ячейка: {self.cell_id}{reserved}"
        )
