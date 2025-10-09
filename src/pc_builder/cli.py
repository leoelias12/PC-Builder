from .catalog import list_top, catalog
from .models import ComputerBuild, Component
from .exceptions import CompatibilityError, InventoryError
from .utils import format_currency
from .catalog import (
    catalog,
    print_cpu_table,
    print_mobo_table,
    print_gpu_table,
    print_ram_table,
    print_psu_table,
    print_storage_table,
    print_case_table
)


def run_menu() -> None:
    print("\nWelcome to PC Builder Configurator (New Generation only)\n")

    # preferences (optional)
    cpu_pref = input("Choose your CPU preference [\033[31mAMD\033[0m/\033[34mIntel\033[0m or Enter for both]: ").strip().title()
    cpu_pref = {"Amd": "AMD", "Intel": "Intel"}.get(cpu_pref, None)

    gpu_pref = input("Choose your GPU preference [\033[32mNVIDIA\033[0m/\033[31mAMD\033[0m or Enter for both]: ").strip().upper()
    gpu_pref = gpu_pref if gpu_pref in {"NVIDIA", "AMD"} else None

    build = ComputerBuild(cpu_brand_pref=cpu_pref, gpu_brand_pref=gpu_pref)

    while True:
        print("\nMenu:\n[1] List CPUs\n[2] List MOBOS\n[3] List GPUs\n[4] List RAM\n"
              "[5] List PSUs\n[6] List Storage\n[7] List Cases\n[8] Add Part\n[9] Summary\n[0] Exit")
        choice = input("Choose: ").strip()

        if choice == "0":
            break

            # ---------- CPUs ----------
        elif choice == "1":
            print_cpu_table(build)


        # ---------- Motherboards ----------
        elif choice == "2":
            print_mobo_table()



        # ---------- GPUs ----------
        elif choice == "3":
            print_gpu_table(build)


        # ---------- RAM ----------
        elif choice == "4":
            print_ram_table()


        # ---------- PSUs ----------
        elif choice == "5":
            print_psu_table()


        # ---------- Storage ----------
        elif choice == "6":
            print_storage_table()


        # ---------- Cases ----------
        elif choice == "7":
            print_case_table()


        # ---------- Add Part ----------
        elif choice == "8":
            valid_categories = {
                "cpu": print_cpu_table,
                "motherboard": print_mobo_table,
                "gpu": print_gpu_table,
                "ram": print_ram_table,
                "psu": print_psu_table,
                "storage": print_storage_table,
                "case": print_case_table,
            }

            while True:
                cat = input("\nCategory (cpu/motherboard/gpu/ram/storage/psu/case) or 'back' to cancel: ").strip().lower()

                if cat == "back":
                    break

                if cat not in valid_categories:
                    print(
                        "⚠️ Invalid category. Please enter a valid one (cpu, motherboard, gpu, ram, psu, storage, case).")
                    continue

                # print available parts
                print(f"\nYou're about to choose a {cat.upper()}. Here are the available options:")
                if cat in {"cpu", "gpu"}:
                    valid_categories[cat](build)
                else:
                    valid_categories[cat]()

                # ask for part ID
                while True:
                    pid = input("Enter Part ID (or 'back' to change category): ").strip().upper()
                    if pid.strip().lower() == "back":
                        break

                    part = next((p for p in catalog[cat] if p["id"] == pid), None)
                    if not part:
                        print("⚠️ Unknown Part ID for this category. Please try again.")
                        continue

                    try:
                        build.add_part(cat, Component(cat, part))
                        print(f"✅ Added {part['name']} to {cat}.")
                    except (CompatibilityError, InventoryError, ValueError) as e:
                        print(f"⚠️ {e}")
                    break
                break


        # ---------- Summary ----------
        elif choice == "9":
            print("\n".join(build.summary_lines()))

        else:
            print("Invalid option.")
