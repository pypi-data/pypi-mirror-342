from thinknet_application_specific_exception import BaseErrorData


class ErrorData(BaseErrorData):
    UTV01 = (11, ValueError, "Input must not be empty or contain only whitespace after stripping.")
    UTV02 = (12, ValueError, "Input has an invalid datetime format. Use ISO format (YYYY-MM-DDTHH:MM:SS+07:00).")
    UTV03 = (13, ValueError, "Invalid format must match 'YYYY-MM-DDTHH:MM:SS+07:00'.")
    UTV04 = (14, ValueError, "milliseconds out of range for platform time_t. The value is too large for conversion.")
    UTT01 = (21, TypeError, "Input must be string type.")
    UTX99 = (99, Exception, "Unspecified or unexpected errors.")
