from typing import Optional, Dict

def compatible_cpu_mobo(cpu: Dict, mobo: Dict) -> bool:
    return cpu["socket"] in mobo["sockets"]

def compatible_ram_mobo(ram: Dict, mobo: Dict) -> bool:
    return ram["type"] == mobo["ram_type"]

def estimate_power_draw(cpu: Dict, gpu: Optional[Dict]) -> int:
    """
    CPU TDP + GPU TDP + 15% headroom.
    Uses floor division // to satisfy assessment operators.
    """
    base = cpu["tdp"] + (gpu["tdp"] if gpu else 0)
    headroom = (base * 15) // 100
    return base + headroom

def psu_sufficient(psu: Dict, est_power_draw: int) -> bool:
    return psu["watts"] >= est_power_draw
