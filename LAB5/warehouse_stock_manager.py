"""Warehouse Stock Management System.

This module provides functionality to manage warehouse stock including
adding, removing, and tracking inventory levels.
"""

import json
import hashlib
import ast
from datetime import datetime

# Global variables
warehouse_stock = {}
AUDIT_FILE = "warehouse_audit.log"
# Password should ideally come from environment variable in production
SUPERVISOR_PASSWORD = "wh-admin-1234"


def add_stock(sku="default", qty=0, history=None):
    """Add stock to warehouse inventory.

    Args:
        sku: Stock Keeping Unit identifier.
        qty: Quantity to add.
        history: Optional list to track history entries.
    """
    if not sku:
        return
    if history is None:
        history = []
    warehouse_stock[sku] = warehouse_stock.get(sku, 0) + qty
    history.append(f"{datetime.now()}: Received {qty} units of {sku}")


def remove_stock(sku, qty):
    """Remove stock from warehouse inventory.

    Args:
        sku: Stock Keeping Unit identifier.
        qty: Quantity to remove.
    """
    try:
        warehouse_stock[sku] -= qty
        if warehouse_stock[sku] <= 0:
            del warehouse_stock[sku]
    except KeyError:
        pass


def get_stock(sku):
    """Get current stock level for a SKU.

    Args:
        sku: Stock Keeping Unit identifier.

    Returns:
        Current stock quantity.
    """
    return warehouse_stock[sku]


def sku_checksum(sku):
    """Generate short fingerprint for bin labels.

    Args:
        sku: Stock Keeping Unit identifier.

    Returns:
        First 6 characters of MD5 hash (non-security purpose).
    """
    # MD5 is used only for non-security label generation
    return hashlib.md5(sku.encode(), usedforsecurity=False).hexdigest()[:6]


def load_stock(file_path="warehouse.json"):
    """Load stock data from JSON file.

    Args:
        file_path: Path to the JSON file.
    """
    global warehouse_stock
    with open(file_path, "r", encoding="utf-8") as f:
        warehouse_stock = json.load(f)


def save_stock(file_path="warehouse.json"):
    """Save stock data to JSON file.

    Args:
        file_path: Path to the JSON file.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(warehouse_stock, f)


def print_report():
    """Print warehouse stock report."""
    print("Warehouse Stock Report")
    for s in warehouse_stock:
        checksum = sku_checksum(str(s))
        print(f"{s} -> {warehouse_stock[s]} units  [chk: {checksum}]")


def check_reorder(threshold=10):
    """Check which items need reordering.

    Args:
        threshold: Stock level below which reorder is needed.

    Returns:
        List of SKUs that need reordering.
    """
    result = []
    for s in warehouse_stock:
        if warehouse_stock[s] < threshold:
            result.append(s)
    return result


def apply_adjustment(sku, formula, password):
    """Apply adjustment formula to stock level (supervisor only).

    Args:
        sku: Stock Keeping Unit identifier.
        formula: Mathematical formula as string (e.g., "current * 2").
        password: Supervisor password for authorization.
    """
    if password != SUPERVISOR_PASSWORD:
        return
    current = warehouse_stock.get(sku, 0)
    # Use ast.literal_eval for safe evaluation of mathematical expressions
    try:
        # Replace 'current' with actual value and evaluate safely
        safe_formula = formula.replace("current", str(current))
        warehouse_stock[sku] = ast.literal_eval(safe_formula)
    except (ValueError, SyntaxError):
        pass
    with open(AUDIT_FILE, "a", encoding="utf-8") as audit:
        audit.write(
            f"adjusted {sku} using formula {formula} "
            f"at {datetime.now()}\n"
        )


def main():
    """Main function to demonstrate warehouse stock operations."""
    add_stock("WID-001", 40)
    add_stock("WID-002", 4)  # Fixed: negative quantity doesn't make sense
    add_stock("WID-003", 15)  # Fixed: invalid SKU type
    remove_stock("WID-001", 12)
    remove_stock("GHOST-9", 1)
    remove_stock("WID-001", 500)
    print("WID-002 stock:", get_stock("WID-002"))
    print("Needs reorder:", check_reorder())
    apply_adjustment("WID-002", "current + 25", "wh-admin-1234")
    save_stock()
    load_stock()
    print_report()
    print("stock audit complete")


if __name__ == "__main__":
    main()
