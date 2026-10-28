"""Pure helpers shared by notebooks and local tests."""

import re

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
VALID_ORDER_STATUSES = {"PROCESSING", "SHIPPED", "COMPLETED", "CANCELLED"}


def customer_errors(row: dict) -> list[str]:
    errors = []
    if not row.get("customer_id"):
        errors.append("MISSING_CUSTOMER_ID")
    if not row.get("full_name"):
        errors.append("MISSING_FULL_NAME")
    if not EMAIL_PATTERN.match(row.get("email") or ""):
        errors.append("INVALID_EMAIL")
    if len(row.get("country_code") or "") != 2:
        errors.append("INVALID_COUNTRY_CODE")
    return errors


def order_errors(row: dict) -> list[str]:
    errors = []
    if not row.get("order_id"):
        errors.append("MISSING_ORDER_ID")
    if not row.get("customer_id"):
        errors.append("MISSING_CUSTOMER_ID")
    if (row.get("quantity") or 0) <= 0:
        errors.append("INVALID_QUANTITY")
    if (row.get("unit_price") or 0) <= 0:
        errors.append("INVALID_UNIT_PRICE")
    if row.get("status") not in VALID_ORDER_STATUSES:
        errors.append("INVALID_STATUS")
    return errors

