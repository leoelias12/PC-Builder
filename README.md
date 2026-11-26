# PC Builder

A command-line PC configurator written in Python, built as my project for the UCD Professional Academy Python Programming course (2025).

The user picks a CPU and GPU brand preference, browses a catalogue of current-generation parts, and adds parts to a build. The app checks that the parts work together and shows a summary with the total price.

## Features
- Menu to list CPUs, motherboards, GPUs, RAM, power supplies, storage and cases
- Brand preferences for CPU (AMD / Intel) and GPU (NVIDIA / AMD)
- Compatibility checks:
  - CPU socket must match the motherboard (AM5 or LGA185x)
  - RAM must match the motherboard memory type (DDR5)
  - Power supply must cover the estimated power draw (CPU + GPU + 15% headroom)
- Build summary with total price and a simple performance score
- Clear error messages for invalid choices (custom exceptions)

## How to run
Requires Python 3.10 or newer. No extra packages needed.

```bash
git clone https://github.com/leoelias12/PC-Builder.git
cd PC-Builder/src
python -m pc_builder.main
```

## Project structure
```
src/pc_builder/
  main.py        entry point
  cli.py         menu and user input
  catalog.py     parts catalogue and tables
  models.py      Component and ComputerBuild classes
  compat.py      compatibility and power rules
  exceptions.py  CompatibilityError, InventoryError
  utils.py       price formatting
```

## What I practised
Python packages and modules, classes and dataclasses, type hints, custom exceptions, input validation and menu-driven CLI design.
