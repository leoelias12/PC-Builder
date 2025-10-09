from typing import Any, Dict, List, Optional

# Intentionally small, current-gen only. Easy to expand later.
Catalog = Dict[str, List[Dict[str, Any]]]

catalog: Catalog = {
    "cpu": [
        # AMD AM5 (Ryzen 9000 series)
        {"id": "AMD1", "brand": "AMD", "name": "Ryzen 7 9700X",
         "price": 349, "socket": "AM5", "tdp": 105, "memory": "DDR5"},
        {"id": "AMD2", "brand": "AMD", "name": "Ryzen 9 9900X",
         "price": 569, "socket": "AM5", "tdp": 170, "memory": "DDR5"},

        # Intel LGA185x (generic placeholders)
        {"id": "INTEL1", "brand": "Intel", "name": "Core i7 (LGA185x)",
         "price": 459, "socket": "LGA185x", "tdp": 125, "memory": "DDR5"},
        {"id": "INTEL2", "brand": "Intel", "name": "Core i9 (LGA185x)",
         "price": 649, "socket": "LGA185x", "tdp": 150, "memory": "DDR5"},
    ],
    "motherboard": [
        # AM5
        {"id": "AMD1", "name": "AM5 X870E ATX", "price": 289,
         "sockets": {"AM5"}, "ram_type": "DDR5", "chipset": "X870E", "form_factor": "ATX"},
        {"id": "AMD2", "name": "AM5 B650 Micro-ATX", "price": 179,
         "sockets": {"AM5"}, "ram_type": "DDR5", "chipset": "B650", "form_factor": "mATX"},

        # LGA185x
        {"id": "INTEL1", "name": "LGA185x Z-Series ATX", "price": 269,
         "sockets": {"LGA185x"}, "ram_type": "DDR5", "chipset": "Z-Series", "form_factor": "ATX"},
        {"id": "INTEL2", "name": "LGA185x B-Series Micro-ATX", "price": 199,
         "sockets": {"LGA185x"}, "ram_type": "DDR5", "chipset": "B-Series", "form_factor": "mATX"},
    ],
    "gpu": [
        # NVIDIA RTX 50
        {"id": "[NVIDIA1]", "brand": "NVIDIA", "name": "GeForce RTX 5070", "price": 549, "tdp": 220},
        {"id": "[NVIDIA2]", "brand": "NVIDIA", "name": "GeForce RTX 5090", "price": 1599, "tdp": 420},

        # AMD RX 8000
        {"id": "[AMD1]", "brand": "AMD", "name": "Radeon RX 8700 XT", "price": 599, "tdp": 260},
        {"id": "[AMD2]", "brand": "AMD", "name": "Radeon RX 8900 XTX", "price": 1199, "tdp": 355},
    ],
    "ram": [
        {"id": "RAM1", "name": "32GB (2x16) DDR5-6000", "price": 109, "type": "DDR5", "speed": 6000},
        {"id": "RAM2", "name": "64GB (2x32) DDR5-6000", "price": 209, "type": "DDR5", "speed": 6000},
    ],
    "psu": [
        {"id": "PSU1", "name": "750W 80+ Gold", "price": 119, "watts": 750},
        {"id": "PSU2", "name": "850W 80+ Gold", "price": 139, "watts": 850},
        {"id": "PSU3","name": "1000W 80+ Gold", "price": 189, "watts": 1000},
    ],
    "storage": [
        {"id": "SSD1", "name": "1TB NVMe Gen4", "price": 69, "type": "NVMe"},
        {"id": "SSD2", "name": "2TB NVMe Gen4", "price": 119, "type": "NVMe"},
    ],
    "case": [
        {"id": "CASE1", "name": "ATX Mid Tower (Airflow)", "price": 89, "form_factor": "ATX"},
        {"id": "CASE2","name": "mATX Compact Tower", "price": 69, "form_factor": "mATX"},
    ],
}

def categories() -> List[str]:
    return list(catalog.keys())

def list_top(category: str, n: int = 5, brand: Optional[str] = None) -> List[Dict[str, Any]]:
    """Top-N listing with optional brand filter (uses slicing for the rubric)."""
    if category not in catalog:
        raise KeyError(f"Invalid category: {category}")
    items = catalog[category]
    if brand:
        items = [x for x in items if x.get("brand") == brand]
    return items[:n]

from .utils import format_currency


# ---------- PRINTING FUNCTIONS ----------

def print_cpu_table(build=None, n: int = 10):
    cpus = list_top("cpu", n, brand=build.cpu_brand_pref if build else None)
    line = "-" * 70
    print()
    print("LIST OF CPUs".center(70, '-'))
    print(line)
    print(f"{'ID':<8} {'MODEL NAME':<21} {'BRAND':<10} {'PRICE':>10} {'SOCKET':>10}")
    print(line)
    for p in cpus:
        print(f"{p['id']:<8} {p['name']:<21} {p['brand']:<10} "
              f"{format_currency(p['price']):>10} {p['socket']:>10}")
    print(line)


def print_mobo_table(n: int = 10):
    mobos = list_top("motherboard", n)
    line = "-" * 86
    print()
    print("LIST OF MOBOs".center(86, '-'))
    print(line)
    print(f"{'ID':<8} {'MODEL NAME':<29} {'CHIPSET':<10} {'FORM':<6} {'RAM':<6} {'PRICE':>10} {'SOCKET':>10}")
    print(line)
    for p in mobos:
        sockets = "/".join(sorted(p["sockets"]))
        print(f"{p['id']:<8} {p['name']:<29} {p['chipset']:<10} {p['form_factor']:<6} {p['ram_type']:<6} "
              f"{format_currency(p['price']):>10} {sockets:>10}")
    print(line)


def print_gpu_table(build=None, n: int = 10):
    gpus = list_top("gpu", n, brand=build.gpu_brand_pref if build else None)
    line = "-" * 70
    print()
    print("LIST OF GPUs".center(70, '-'))
    print(line)
    print(f"{'ID':<10} {'MODEL NAME':<25} {'BRAND':<10} {'PRICE':>10} {'TDP':>6}")
    print(line)
    for p in gpus:
        print(f"{p['id']:<10} {p['name']:<25} {p['brand']:<10} "
              f"{format_currency(p['price']):>10} {p['tdp']:>5}W")
    print(line)


def print_ram_table(n: int = 10):
    rams = list_top("ram", n)
    line = "-" * 64
    print()
    print("LIST OF RAMs".center(64, '-'))
    print(line)
    print(f"{'ID':<8} {'MODEL NAME':<25} {'TYPE':<6} {'SPEED':>7} {'PRICE':>10}")
    print(line)
    for p in rams:
        print(f"{p['id']:<8} {p['name']:<25} {p['type']:<6} "
              f"{str(p['speed']) + 'MT/s':>7} {format_currency(p['price']):>10}")
    print(line)


def print_psu_table(n: int = 10):
    psus = list_top("psu", n)
    line = "-" * 55
    print()
    print("LIST OF PSUs".center(55, '-'))
    print(line)
    print(f"{'ID':<8} {'MODEL NAME':<25} {'WATTS':>7} {'PRICE':>10}")
    print(line)
    for p in psus:
        print(f"{p['id']:<8} {p['name']:<25} {str(p['watts']) + 'W':>7} {format_currency(p['price']):>10}")
    print(line)


def print_storage_table(n: int = 10):
    ssds = list_top("storage", n)
    line = "-" * 52
    print()
    print("LIST OF STORAGES".center(52, '-'))
    print(line)
    print(f"{'ID':<8} {'MODEL NAME':<25} {'TYPE':<6} {'PRICE':>10}")
    print(line)
    for p in ssds:
        print(f"{p['id']:<8} {p['name']:<25} {p['type']:<6} {format_currency(p['price']):>10}")
    print(line)


def print_case_table(n: int = 10):
    cases = list_top("case", n)
    line = "-" * 55
    print()
    print("LIST OF CASES".center(55, '-'))
    print(line)
    print(f"{'ID':<8} {'MODEL NAME':<25} {'FORM':<6} {'PRICE':>10}")
    print(line)
    for p in cases:
        print(f"{p['id']:<8} {p['name']:<25} {p['form_factor']:<6} {format_currency(p['price']):>10}")
    print(line)
