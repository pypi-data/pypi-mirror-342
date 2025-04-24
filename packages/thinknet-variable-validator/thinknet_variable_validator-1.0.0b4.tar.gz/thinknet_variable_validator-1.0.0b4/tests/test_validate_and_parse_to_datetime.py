from datetime import datetime
import pytest
from thinknet_application_specific_exception import ApplicationSpecificException
from thinknet_variable_validator import validate_and_parse_to_datetime

def test_validate_and_parse_to_datetime():
    dt = "2024-01-01T07:00:00Z"
    result = validate_and_parse_to_datetime(dt)
    assert result == datetime(2024,1,1,7,0,0)

def test_non_str_variable():
    dt = 20240101

    with pytest.raises(ApplicationSpecificException) as excinfo:
        validate_and_parse_to_datetime(dt)

    assert excinfo.value.error_code == "UTT01"
    assert excinfo.value.input_params == {"value":dt}

def test_wrong_datetime_format_variable():
    dt = "2024-01-01 07:00:00Z"

    with pytest.raises(ApplicationSpecificException) as excinfo:
        validate_and_parse_to_datetime(dt)

    assert excinfo.value.error_code == "UTV02"
    assert excinfo.value.input_params == {"value":dt, 'value_stripped': dt}