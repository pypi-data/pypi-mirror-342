import os
from dataclasses import dataclass
from datetime import datetime

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

@dataclass
class RecordData:
    abbr: str = None
    driver: str = None
    team: str = None
    _start: datetime = None
    _stop: datetime = None
    _lap_time_seconds: int = None
    error: list[dict[str, str]] = None

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value

    @property
    def stop(self):
        return self._stop

    @stop.setter
    def stop(self, value):
        self._stop = value

    @property
    def lap_time_seconds(self):
        return self._lap_time_seconds

    @lap_time_seconds.setter
    def lap_time_seconds(self, value):
        if float(value) <= 0:
            error_value = {self.abbr: ERR_MSG__LAP_TIME_ZERO_OR_NEGATIVE}
            if self.error is None:
                self.error = []
            self.error.append(error_value)
        else:
            self._lap_time_seconds = value

    def __str__(self):
        return (
            f"RecordData("
            f"abbr='{self.abbr}', "
            f"driver='{self.driver}', "
            f"team='{self.team}', "
            f"start='{self.start}', "
            f"stop='{self.stop}', "
            f"lap_time_seconds={self.lap_time_seconds}, "
            f"error={self.error}"
            f")"
        )


def _is_valid_datetime(value: str, datetime_format: str = "%Y-%m-%d_%H:%M:%S.%f") -> bool:
    try:
        datetime.strptime(value, datetime_format)
        return True
    except ValueError:
        return False


def _validate_if_file_exists(filepath) -> bool:
    """Check if the folder and file exist, raise error if not."""
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    folder = os.path.dirname(filepath)
    if folder and not os.path.exists(folder):
        raise FileNotFoundError(f"Folder does not exist: {folder}")
    return True


def _validate_abbreviation_row(row: str) -> RecordData:
    match = ABBR_ROW_PATTERN.match(row)
    if match:
        driver_entry = RecordData(abbr=match.group('abbr'), driver=match.group('driver'), team=match.group('team'))
        return driver_entry

    return None


def _validate_start_stop_row(row: str) -> (str, datetime):
    match = START_STOP_ROW_PATTERN.match(row)
    if match:
        abbr = match.group('abbr')
        time_event_raw = match.group('time_event')
        if _is_valid_datetime(time_event_raw):
            time_event = datetime.strptime(time_event_raw, "%Y-%m-%d_%H:%M:%S.%f")
            event_time_out = (abbr, time_event)
            return event_time_out

    print(f"discard row: [{row}], because {ERR_MSG__INVALID_FORMAT_OF_TIME_EVENT_ROW}")
    return None  # if start or stop row has invalid then a row is discarded


def _create_driver_record(row) -> RecordData:
    record_driver_out = _validate_abbreviation_row(row)
    if record_driver_out is None:
        error_val = {row: ERR_PREFIX}
        record_driver_out = RecordData(error=[error_val])
    return record_driver_out


def _read_file_abbreviation(filepath) -> list[dict[str, RecordData], dict[str, RecordData]]:
    dict_records_good = dict()
    dict_records_bad = dict()
    with open(filepath, 'r', encoding='utf-8') as file:
        for line_numerator, line in enumerate(file, start=1):
            row = line.strip()

            if not row:
                continue  # skip empty lines
            driver_record = _create_driver_record(row)

            if not driver_record.error:
                dict_records_good[driver_record.abbr] = driver_record
            else:
                key_invalid_row = str(ERR_PREFIX + str(line_numerator))
                dict_records_bad[key_invalid_row] = driver_record
    return [dict_records_good, dict_records_bad]


def _read_file_start_stop(filepath: str) -> dict[str, datetime]:
    dict_out = dict()
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue  # Skip empty lines

            time_event_record = _validate_start_stop_row(line)

            if time_event_record is not None:
                abbr = time_event_record[0]
                time_event = time_event_record[1]
                dict_out[abbr] = time_event
    return dict_out


def build_report(
        folder: str,
        file_abbr: str,
        file_start: str,
        file_stop: str,
) -> tuple[list[RecordData], list[RecordData]]:
    filepath_abbr = os.path.join(os.path.dirname(__file__), folder, file_abbr)
    filepath_start = os.path.join(os.path.dirname(__file__), folder, file_start)
    filepath_stop = os.path.join(os.path.dirname(__file__), folder, file_stop)
    list_records_good = list()
    list_records_bad = list()

    if (_validate_if_file_exists(filepath_abbr)) and (_validate_if_file_exists(filepath_start)) and (
            _validate_if_file_exists(filepath_stop)):
        [dict_records_good, dict_records_bad] = _read_file_abbreviation(filepath_abbr)

        dict_start = _read_file_start_stop(filepath=filepath_start)
        dict_stop = _read_file_start_stop(filepath=filepath_stop)

        for key_abbr, val_abbr in dict_records_good.items():
            driver_record_current = dict_records_good[key_abbr]
            key_start_time = dict_start[key_abbr]
            key_stop_time = dict_stop[key_abbr]

            if key_start_time and key_stop_time:
                driver_record_current.start = key_start_time
                driver_record_current.stop = key_stop_time
                lap_time_seconds = (key_stop_time - key_start_time).total_seconds()
                driver_record_current.lap_time_seconds = lap_time_seconds
                list_records_good.append(driver_record_current)
            else:
                list_records_bad.append()

        for k in dict_records_bad:
            list_records_bad.append(dict_records_bad[k])

        # error values can be assigned in the property [lap_time_seconds]. I check if there are any Records with errors:
        for key_abbr, val_abbr in dict_records_good.items():
            driver_record_current = dict_records_good[key_abbr]
            if driver_record_current.error is not None:
                list_records_good.remove(driver_record_current)
                list_records_bad.append(driver_record_current)
    output = [list_records_good, list_records_bad]

    return output


def print_report(records_good: list[RecordData], records_bad: list[RecordData], sort_by_lap_asc: bool = True):
    print(f"---------RACE REPORT OF GOOD RECORDS--------------")
    if sort_by_lap_asc:
        sorted_good_records = sorted(records_good, key=lambda r: r.lap_time_seconds, reverse=False)
    else:
        sorted_good_records = sorted(records_good, key=lambda r: r.lap_time_seconds, reverse=True)

    for j in sorted_good_records:
        print(j)

    if records_bad:
        print(f"---------RACE REPORT OF INVALID RECORDS--------------")
        for j in records_bad:
            print(j)


def main_run():
    folder = 'data'
    file_abbr = 'abbreviations.txt'
    file_start = 'start.log'
    file_stop = 'end.log'

    data_report = build_report(folder=folder, file_abbr=file_abbr, file_start=file_start, file_stop=file_stop)
    print_report(records_good=data_report[0], records_bad=data_report[1], sort_by_lap_asc=False)


if __name__ == '__main__':
    main_run()
