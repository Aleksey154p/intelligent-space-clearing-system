"""
cell.py — модель ячейки хранения

Данные приходят из SAP в виде JSON:
{
    "cell_id":    "P105",
    "capacity":   21,
    "eo_list":    ["7210000126042964", "7210000126042965"],
    "is_blocked": False
}
"""

from dataclasses import dataclass, field


@dataclass
class Cell:
    cell_id: str
    capacity: int  # максимум паллетов
    eo_list: list[str] = field(default_factory=list)  # список eo_id
    is_blocked: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> "Cell":
        """Создать Cell из словаря (распарсенного JSON из SAP)"""
        return cls(
            cell_id=data["cell_id"],
            capacity=data["capacity"],
            eo_list=list(data.get("eo_list", [])),
            is_blocked=data.get("is_blocked", False),
        )

    def to_dict(self) -> dict:
        """Сериализовать Cell обратно в словарь"""
        return {
            "cell_id": self.cell_id,
            "capacity": self.capacity,
            "eo_list": self.eo_list,
            "is_blocked": self.is_blocked,
        }

    @property
    def occupancy(self) -> int:
        """Сколько паллетов сейчас в ячейке"""
        return len(self.eo_list)

    @property
    def free_space(self) -> int:
        """Сколько свободных мест"""
        return self.capacity - self.occupancy

    @property
    def occupancy_pct(self) -> float:
        """Заполненность в процентах"""
        if self.capacity == 0:
            return 0.0
        return self.occupancy / self.capacity * 100

    @property
    def is_available(self) -> bool:
        """Ячейка доступна для размещения - не заблокирована и есть место"""
        return not self.is_blocked and self.free_space > 0

    def __str__(self) -> str:
        status = "ЗАБЛОКИРОВАНА" if self.is_blocked else f"{self.occupancy}/{self.capacity}"
        return f"Cell {self.cell_id} [{status}]"
