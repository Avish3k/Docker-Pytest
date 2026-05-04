from utils import validate_task

def test_valid_task():
    valid, _ = validate_task("Buy milk")
    assert valid is True

def test_empty_title():
    valid, msg = validate_task("")
    assert valid is False