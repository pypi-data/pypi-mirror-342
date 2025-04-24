import pytest
from thinknet_application_specific_exception import ApplicationSpecificException
from thinknet_variable_validator import convert_unix_timestamp_ms_to_thai_isodate

def test_convert_unix_timestamp_ms_to_thai_isodate_different_timestamps():
    test_cases = [
        (0, "1970-01-01 07:00:00"),
        (1577836800000, "2020-01-01 07:00:00"),
        (1640995200000, "2022-01-01 07:00:00")
    ]

    for millis, expected in test_cases:
        assert convert_unix_timestamp_ms_to_thai_isodate(millis) == expected

def test_convert_unix_timestamp_ms_to_thai_isodate_overflow():
    with pytest.raises(ApplicationSpecificException) as excinfo:
        convert_unix_timestamp_ms_to_thai_isodate(2**63)

    assert excinfo.value.error_code == "UTV04"
    assert excinfo.value.input_params == {"millis":2**63}

def test_convert_unix_timestamp_ms_to_thai_isodate_negative_millis():
    millis = -1000  # 1 second before Unix epoch
    result = convert_unix_timestamp_ms_to_thai_isodate(millis)
    assert result == "1970-01-01 06:59:59"
