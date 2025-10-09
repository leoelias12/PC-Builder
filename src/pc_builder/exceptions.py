class CompatibilityError(Exception):
    """Raised when selected components are incompatible."""


class InventoryError(Exception):
    """Raised when a requested component/category is invalid."""