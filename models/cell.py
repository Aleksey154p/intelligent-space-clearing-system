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
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.eo import EO


@dataclass
class Cell:
    cell_id: str
    capacity: int  # вместимость в ячейке
    eo_list: list["EO"] = field(default_factory=list)  # список eo_id
    is_blocked: bool = False

    @property
    def occupancy(self) -> int:
        """Сколько паллетов сейчас в ячейке"""
        return len(self.eo_list)

    @property
    def free_space(self) -> int:
        """Сколько свободных мест"""
        return self.capacity - self.occupancy

    # В дальнейшем будет использоваться для
    # контроля над утилизацией ячеек, в которые будут освобождаться ЕО
    # из целевой ячейки

    # @property
    # def occupancy_percent(self) -> float:
    #     """Заполненность в процентах"""
    #     if self.capacity == 0:
    #         return 0.0
    #     return self.occupancy / self.capacity * 100

    @property
    def is_available(self) -> bool:
        """Ячейка доступна для размещения - не заблокирована и есть место"""
        return not self.is_blocked and self.free_space > 0

    def __str__(self) -> str:
        status = "ЗАБЛОКИРОВАНА" if self.is_blocked else f"{self.occupancy}/{self.capacity}"
        return f"Cell {self.cell_id} [{status}]"
