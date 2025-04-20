from datetime import datetime
from unittest.mock import mock_open, patch
import pytest
import src.utilities as util
from src.race_report import _read_file_abbreviation, RecordData, _read_file_start_stop
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


def test_read_abbreviation__basic():
    mock_file_content = "SVF_Sebastian Vettel_Ferrari\nLHM_Lewis Hamilton_Mercedes\n"
    m = mock_open(read_data=mock_file_content)

    with patch("builtins.open", m):
        result = _read_file_abbreviation("fake_path.txt")  # path doesn't matter when mocking

    assert isinstance(result, dict)
    assert len(result) == 2
    assert result['SVF'] == RecordData('SVF', 'Sebastian Vettel', 'Ferrari')
    assert result['LHM'] == RecordData('LHM', 'Lewis Hamilton', 'Mercedes')


def test_read_abbreviation__wrong_path():
    mock_file_content = "SVF_Sebastian Vettel\n"
    mock_file_path = "wrong_path_of_file.txt"
    m = mock_open(read_data=mock_file_content)

    with patch("builtins.open", m):
        with pytest.raises(ValueError):
            _read_file_abbreviation(mock_file_path)


def test_read_start_stop__basic():
    mock_file_content = "SVF2018-05-24_12:02:58.917\nLHM2018-05-24_12:03:01.035\n"
    m = mock_open(read_data=mock_file_content)

    with patch("builtins.open", m):
        result = _read_file_start_stop("fake_path.txt")

    assert isinstance(result, dict)
    assert len(result) == 2
    assert result['SVF'] == datetime(2018, 5, 24, 12, 2, 58, 917000)
    assert result['LHM'] == datetime(2018, 5, 24, 12, 3, 1, 35000)


def test_read_start_stop__invalid_datetime_format():
    mock_file_content = "SVF24-05-2018 12:02:58.917\n"  # Wrong format
    m = mock_open(read_data=mock_file_content)

    with patch("builtins.open", m):
        with pytest.raises(ValueError):
            _read_file_start_stop("invalid_file.txt")


def test_validate_if_file_exists__success():
    filepath = "/fake/path/to/file.txt"

    with patch("os.path.isfile", return_value=True), \
            patch("os.path.exists", return_value=True):
        assert util._validate_if_file_exists(filepath) is True


def test_validate_if_file_exists__file_missing_but_folder_exists():
    filepath = "/existing/folder/missing_file.txt"

    with patch("os.path.isfile", return_value=False), \
            patch("os.path.exists", return_value=True):
        with pytest.raises(FileNotFoundError, match="File not found"):
            util._validate_if_file_exists(filepath)


def test_validate_if_file_exists__folder_missing_but_file_mocked_as_present():
    filepath = "/missing_folder/file.txt"

    with patch("os.path.isfile", return_value=True), \
            patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError, match="Folder does not exist"):
            util._validate_if_file_exists(filepath)


def test_validate_if_file_exists__file_and_folder_missing():
    filepath = "/missing_folder/missing_file.txt"

    with patch("os.path.isfile", return_value=False), \
            patch("os.path.exists", return_value=False):  # won't be reached
        with pytest.raises(FileNotFoundError, match="File not found"):
            util._validate_if_file_exists(filepath)
