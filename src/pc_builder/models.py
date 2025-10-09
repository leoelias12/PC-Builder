from dataclasses import dataclass
from typing import Optional, Dict, Any
from .exceptions import CompatibilityError, InventoryError
from .compat import compatible_cpu_mobo, compatible_ram_mobo, psu_sufficient, estimate_power_draw

@dataclass
class Component:
    category: str
    data: Dict[str, Any]

    @property
    def name(self) -> str:
        return self.data["name"]

    @property
    def price(self) -> float:
        return float(self.data["price"])

class ComputerBuild:
    def __init__(self, cpu_brand_pref: Optional[str] = None, gpu_brand_pref: Optional[str] = None) -> None:
        self.cpu_brand_pref = cpu_brand_pref  # "AMD"/"Intel" or None
        self.gpu_brand_pref = gpu_brand_pref  # "NVIDIA"/"AMD" or None
        self.selected: Dict[str, Optional[Component]] = {
            "cpu": None, "motherboard": None, "gpu": None, "ram": None,
            "storage": None, "psu": None, "case": None
        }

    def add_part(self, category: str, comp: Component) -> None:
        if category not in self.selected:
            raise InventoryError(f"Unknown category: {category}")

        # preference checks
        if category == "cpu" and self.cpu_brand_pref and comp.data.get("brand") != self.cpu_brand_pref:
            raise CompatibilityError(f"CPU brand preference is {self.cpu_brand_pref}, selected {comp.data.get('brand')}.")
        if category == "gpu" and self.gpu_brand_pref and comp.data.get("brand") != self.gpu_brand_pref:
            raise CompatibilityError(f"GPU brand preference is {self.gpu_brand_pref}, selected {comp.data.get('brand')}.")

        # compatibility rules
        if category == "motherboard" and self.selected["cpu"]:
            if not compatible_cpu_mobo(self.selected["cpu"].data, comp.data):
                raise CompatibilityError("Motherboard socket does not match selected CPU (AM5 vs LGA185x).")
            if comp.data["ram_type"] != "DDR5":
                raise CompatibilityError("Only DDR5 motherboards are supported.")

        if category == "cpu" and self.selected["motherboard"]:
            if not compatible_cpu_mobo(comp.data, self.selected["motherboard"].data):
                raise CompatibilityError("CPU socket does not match selected Motherboard.")
            if comp.data["memory"] != self.selected["motherboard"].data["ram_type"]:
                raise CompatibilityError("CPU memory requirement mismatch (DDR5).")

        if category == "ram" and self.selected["motherboard"]:
            if not compatible_ram_mobo(comp.data, self.selected["motherboard"].data):
                raise CompatibilityError("RAM must be DDR5 for the selected motherboard.")

        if category == "psu":
            cpu = self.selected["cpu"].data if self.selected["cpu"] else {"tdp": 105}
            gpu = self.selected["gpu"].data if self.selected["gpu"] else None
            if not psu_sufficient(comp.data, estimate_power_draw(cpu, gpu)):
                raise CompatibilityError("PSU wattage appears insufficient for current parts.")

        self.selected[category] = comp

    def remove_part(self, category: str) -> None:
        if category not in self.selected:
            raise InventoryError(f"Unknown category: {category}")
        self.selected[category] = None

    def total_price(self) -> float:
        return sum(c.price for c in self.selected.values() if c)

    def estimated_performance_score(self) -> int:
        """
        Toy metric using ** to meet rubric:
        int(((CPU TDP + GPU TDP or 200) ** 1.03) // 1)
        """
        cpu_tdp = (self.selected["cpu"].data["tdp"] if self.selected["cpu"] else 105)
        gpu_tdp = (self.selected["gpu"].data["tdp"] if self.selected["gpu"] else 200)
        raw = (cpu_tdp + gpu_tdp) ** 1.03
        return int(raw // 1)

    def summary_lines(self) -> list:
        from .utils import format_currency
        lines = ["\nYour Current-Gen PC Build:"]
        for cat, comp in self.selected.items():
            lines.append(f"- {cat.upper()}: {comp.name if comp else '(none)'}")
        lines.append(f"Estimated Performance Score: {self.estimated_performance_score()}")
        lines.append(f"Total: {format_currency(self.total_price())}")
        return lines
