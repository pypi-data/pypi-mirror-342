import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from smtp_checker import check_smtp

def test_check_smtp_valid():
    result = check_smtp("smtp.gmail.com")
    assert result == True

def test_check_smtp_invalid():
    result = check_smtp("invalid-smtp.com")
    assert result == False
