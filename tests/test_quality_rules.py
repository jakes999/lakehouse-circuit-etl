from src.quality_rules import customer_errors, order_errors


def test_valid_customer():
    row = {"customer_id": "C001", "full_name": "Amina Patel", "email": "a@example.test", "country_code": "GB"}
    assert customer_errors(row) == []


def test_bad_customer_is_flagged():
    row = {"customer_id": "", "full_name": "", "email": "bad", "country_code": "United Kingdom"}
    assert set(customer_errors(row)) == {"MISSING_CUSTOMER_ID", "MISSING_FULL_NAME", "INVALID_EMAIL", "INVALID_COUNTRY_CODE"}


def test_valid_order():
    row = {"order_id": "O1", "customer_id": "C1", "quantity": 2, "unit_price": 5.0, "status": "COMPLETED"}
    assert order_errors(row) == []


def test_bad_order_is_flagged():
    row = {"order_id": "O1", "customer_id": "C1", "quantity": -1, "unit_price": 0, "status": "UNKNOWN"}
    assert set(order_errors(row)) == {"INVALID_QUANTITY", "INVALID_UNIT_PRICE", "INVALID_STATUS"}

