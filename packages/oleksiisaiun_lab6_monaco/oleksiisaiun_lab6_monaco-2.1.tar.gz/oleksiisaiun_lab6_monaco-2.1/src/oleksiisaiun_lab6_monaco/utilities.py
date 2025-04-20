import os
from datetime import datetime
from race_report import RecordData
from constants import ABBR_ROW_PATTERN,START_STOP_ROW_PATTERN,ERR_MSG__INVALID_FORMAT_OF_TIME_EVENT_ROW

def is_valid_datetime(value: str, datetime_format: str = "%Y-%m-%d_%H:%M:%S.%f") -> bool:
    try:
        datetime.strptime(value, datetime_format)
        return True
    except ValueError:
        return False

def validate_if_file_exists(filepath) -> bool:
    """Check if the folder and file exist, raise error if not."""
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    folder = os.path.dirname(filepath)
    if folder and not os.path.exists(folder):
        raise FileNotFoundError(f"Folder does not exist: {folder}")
    return True


def validate_abbreviation_row(row: str) -> RecordData:
    match = ABBR_ROW_PATTERN.match(row)
    if match:
        driver_entry = RecordData(abbr=match.group('abbr'), driver=match.group('driver'), team=match.group('team'))
        return driver_entry

    return None

def validate_start_stop_row(row: str) -> (str, datetime):
    match = START_STOP_ROW_PATTERN.match(row)
    if match:
        abbr = match.group('abbr')
        time_event_raw=match.group('time_event')
        if is_valid_datetime(time_event_raw):
            time_event = datetime.strptime(time_event_raw, "%Y-%m-%d_%H:%M:%S.%f")
            event_time_out = (abbr, time_event)
            return event_time_out

    print(f"discard row: [{row}], because {ERR_MSG__INVALID_FORMAT_OF_TIME_EVENT_ROW}")
    return None  # if start or stop row has invalid then a row is discarded
