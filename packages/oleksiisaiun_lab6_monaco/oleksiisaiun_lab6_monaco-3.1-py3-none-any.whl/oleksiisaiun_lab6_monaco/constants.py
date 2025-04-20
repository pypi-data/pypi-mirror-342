import re


ABBR_ROW_PATTERN = re.compile(
    r"^(?P<abbr>[A-Z]{3})_(?P<driver>[A-Za-z .'-]+)_(?P<team>[A-Z0-9 &'()-]+)$"
)


START_STOP_ROW_PATTERN = re.compile(
    r'^(?P<abbr>[A-Z]{3})(?P<time_event>\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2}\.\d{3})$'
)

ERR_MSG__LAP_TIME_ZERO_OR_NEGATIVE="LAP_TIME_CAN_NOT_BE_ZERO_OR_NEGATIVE"
ERR_MSG__EMPTY_START_OR_STOP_TIME="EMPTY_START_OR_STOP_TIME"
ERR_MSG__INVALID_FORMAT_OF_TIME_EVENT_ROW ='INVALID_FORMAT_OF_TIME_EVENT_ROW'
ERR_PREFIX='INVALID_ABBREVIATION_ROW_'