from datetime import datetime
import pytz
from thinknet_application_specific_exception import raise_error
from thinknet_variable_validator.error_data import ErrorData


def convert_unix_timestamp_ms_to_thai_isodate(unix_timestamp_ms: int) -> str:
    try:
        unix_timestamp_seconds = unix_timestamp_ms / 1000
        utc_time = datetime.fromtimestamp(unix_timestamp_seconds, pytz.UTC)
        thailand_time = utc_time.astimezone(pytz.timezone("Asia/Bangkok"))
        formatted_time = thailand_time.isoformat(timespec="seconds")
    except ValueError:
        raise_error(ErrorData.UTV04, {"unix_timestamp_ms": unix_timestamp_ms})
    return formatted_time


def validate_and_strip_str_variable(value: str) -> str:
    if not isinstance(value, str):
        raise_error(ErrorData.UTT01, {"value": value})
    value_stripped = value.strip()
    if not value_stripped:
        raise_error(ErrorData.UTV01, {"value": value, "value_stripped": value_stripped})
    return value_stripped


def validate_and_parse_to_datetime(value: str) -> datetime:
    value_stripped = validate_and_strip_str_variable(value)

    try:
        parsed_datetime = datetime.fromisoformat(value_stripped)
    except ValueError:
        raise_error(
            ErrorData.UTV02,
            {"value": value, "value_stripped": value_stripped},
        )
    return parsed_datetime


def validate_and_check_format_datetime(value: str) -> str:
    value_stripped = validate_and_strip_str_variable(value)

    try:
        datetime.fromisoformat(value_stripped)
    except ValueError:
        raise_error(ErrorData.UTV03, {"value": value, "value_stripped": value_stripped})
    return value_stripped
