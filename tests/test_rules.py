import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from rules_engine import RulesEngine

@pytest.fixture
def rules():
    return RulesEngine()

def test_standardize_date_valid(rules):
    assert rules.standardize_date("January 1, 2025") == "2025-01-01"
    assert rules.standardize_date("01/01/25") == "2025-01-01"
    
def test_standardize_date_invalid(rules):
    assert rules.standardize_date("Not a date") is None
    
def test_standardize_money(rules):
    assert rules.standardize_money("$50,000") == "50000"
    assert rules.standardize_money("20.50 USD") == "20.50"
    
def test_validate_entities_valid_constraints(rules):
    entities = {
        "EFFECTIVE_DATE": ["January 1, 2025"],
        "TERMINATION_DATE": ["December 31, 2026"],
        "MONEY": ["$100,000.50"]
    }
    
    cleaned = rules.validate_entities(entities)
    
    assert cleaned.get("WARNING") is None
    assert cleaned["EFFECTIVE_DATE_ISO"] == "2025-01-01"
    assert cleaned["TERMINATION_DATE_ISO"] == "2026-12-31"
    assert cleaned["MONEY_CLEANED"] == "100000.50"
    
def test_validate_entities_invalid_constraints(rules):
    # Termination date before Effective date
    entities = {
        "EFFECTIVE_DATE": ["December 31, 2026"],
        "TERMINATION_DATE": ["January 1, 2025"]
    }
    
    cleaned = rules.validate_entities(entities)
    
    assert cleaned.get("WARNING") == "Termination Date precedes Effective Date"
