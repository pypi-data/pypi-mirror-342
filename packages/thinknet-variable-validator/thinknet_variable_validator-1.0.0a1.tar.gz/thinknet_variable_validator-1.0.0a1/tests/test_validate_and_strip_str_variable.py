import pytest
from thinknet_application_specific_exception import ApplicationSpecificException
from thinknet_variable_validator import validate_and_strip_str_variable

def test_validate_and_strip_str_variable():
    s = "abc1234"
    result = validate_and_strip_str_variable(s)
    assert result == s

def test_include_whitespace_variable():
    s = "abc 1234 "
    result = validate_and_strip_str_variable(s)
    assert result == "abc 1234"

def test_non_str_variable():
    s = 1234

    with pytest.raises(ApplicationSpecificException) as excinfo:
        validate_and_strip_str_variable(s)

    assert excinfo.value.error_code == "UTT01"
    assert excinfo.value.input_params == {"value":s}

def test_empty_variable():
    s = ""

    with pytest.raises(ApplicationSpecificException) as excinfo:
        validate_and_strip_str_variable(s)

    assert excinfo.value.error_code == "UTV01"
    assert excinfo.value.input_params == {"value":s, "value_stripped": ""}

def test_only_whitespace_variable():
    s = "      "

    with pytest.raises(ApplicationSpecificException) as excinfo:
        validate_and_strip_str_variable(s)

    assert excinfo.value.error_code == "UTV01"
    assert excinfo.value.input_params == {"value":s, "value_stripped": ""}