import pytest

from datetime import datetime, timedelta

from pathlib import Path

from unittest.mock import patch, mock_open, MagicMock

from src.monaco_qualifying import RecordData


@pytest.mark.parametrize(
    "start, stop, expected_duration, expected_errors",
    [
        (
            datetime(2018, 5, 24, 12, 2, 58, 917),
            datetime(2018, 5, 24, 12, 4, 3, 332),  # SVF
            timedelta(seconds=64, microseconds=999415),
            [],
        ),
        (
            datetime(2018, 5, 24, 12, 5, 0),
            datetime(2018, 5, 24, 12, 0, 0),
            None,
            ["Start time is later than or equal to stop time."],
        ),
        (
            None,
            datetime(2018, 5, 24, 12, 4, 3, 332),
            None,
            ["Missing start or stop time."],
        ),
        (
            datetime(2018, 5, 24, 12, 2, 58, 917),
            None,
            None,
            ["Missing start or stop time."],
        ),
    ],
)
def test_duration(start, stop, expected_duration, expected_errors):
    record = RecordData(start=start, stop=stop)
    assert record.duration == expected_duration
    assert record.errors == expected_errors


@pytest.mark.parametrize(
    "line, expected_result",
    [
        ("SVF_Sebastian Vettel_FERRARI", ("SVF", "Sebastian Vettel", "FERRARI")),
        ("NHR_Nico Hulkenberg_RENAULT", ("NHR", "Nico Hulkenberg", "RENAULT")),
        ("INVALID_FORMAT", None),
    ],
)
def test_read_abbreviation(line, expected_result):
    m = mock_open(read_data=f"{line}\n")

    mock_folder = Path("mock_folder")
    mock_file = Path("abbreviations.txt")

    with (
        patch("builtins.open", m),
        patch.object(Path, "exists", return_value=True),
        patch.object(Path, "is_file", return_value=True),
    ):
        result = RecordData._read_abbreviation(mock_folder, mock_file)

    if expected_result:
        abbr, driver, team = expected_result
        assert abbr in result
        assert result[abbr].driver == driver
        assert result[abbr].team == team
    else:
        assert any(k.startswith("ERROR_") for k in result)


@pytest.mark.parametrize(
    "line, expected_error",
    [
        ("SVF2018-05-24_12:02:58.917", None),  # правильний формат
        (
            "XYZ2018-05-24_12:60:00.000",
            "Incorrect timestamp: 2018-05-24_12:60:00.000",
        ),  # неправильний час
    ],
)
def test_read_start_stop(line, expected_error):
    mock_file = MagicMock()
    mock_file.__enter__.return_value = [line]

    mock_folder = MagicMock(spec=Path)
    mock_folder.exists.return_value = True

    with patch("builtins.open", return_value=mock_file):
        records_dict = RecordData._read_start_stop({}, mock_folder, Path("start.log"))

    if expected_error:  # якщо очікується помилка
        errors = [  # пошук помилки у всіх записах
            err for record in records_dict.values() for err in record.errors
        ]
        assert expected_error in errors
    else:
        abbr = line[:3]
        assert abbr in records_dict  # абр в словнику
        assert not records_dict[abbr].errors  # помилок бути не повинно
        expected_datetime = datetime.strptime(line[3:], "%Y-%m-%d_%H:%M:%S.%f")
        assert (
            records_dict[abbr].start == expected_datetime
        )  # перевірка правильної дати


@pytest.mark.parametrize(
    "good_records, invalid_records, expected_parts",
    [
        (
            [
                RecordData(
                    driver="Sebastian Vettel",
                    team="FERRARI",
                    start=datetime(2018, 5, 24, 12, 2, 58, 917),
                    stop=datetime(2018, 5, 24, 12, 4, 3, 332),
                )
            ],
            [],
            ["VALID RESULTS", "Sebastian Vettel", "FERRARI", "1:4.999"],
        ),
        (
            [],
            [
                (lambda r: r.errors.append("Missing start or stop time.") or r)(
                    RecordData(driver="Unknown Driver", team="Unknown")
                )
            ],
            [
                "INVALID RECORDS",
                "Unknown Driver",
                "Unknown",
                "N/A",
                "Missing start or stop time.",
            ],
        ),
    ],
)
def test_print_report(good_records, invalid_records, expected_parts, capsys):
    RecordData.print_report(good_records, invalid_records)
    captured = capsys.readouterr()
    output = captured.out.strip()
    for part in expected_parts:
        assert part in output, f"'{part}' not found in output: {output}"


@patch("src.monaco_qualifying.driver_3_version.RecordData._read_abbreviation")
@patch("src.monaco_qualifying.driver_3_version.RecordData._read_start_stop")
def test_build_report(mock_read_start_stop, mock_read_abbreviation):
    mock_read_abbreviation.return_value = {
        "SVF": RecordData(abbr="SVF", driver="Sebastian Vettel", team="FERRARI")
    }
    mock_read_start_stop.return_value = {
        "SVF": RecordData(
            abbr="SVF",
            driver="Sebastian Vettel",
            team="FERRARI",
            start=datetime(2018, 5, 24, 12, 2, 58, 917),
            stop=datetime(2018, 5, 24, 12, 4, 3, 332),
        )
    }

    record = RecordData()
    good_records, bad_records = record.build_report(
        folder=Path("/"),
        file=Path("abbreviations.txt"),
        start_file=Path("start.log"),
        stop_file=Path("end.log"),
        asc=True,
    )

    assert len(good_records) == 1
    assert good_records[0].driver == "Sebastian Vettel"
    assert len(bad_records) == 0


@patch(
    "sys.argv",
    new=[
        "",
        "--files",
        "abbreviations.txt",
        "start.log",
        "end.log",
        "--asc",
        "--driver",
        "SVF",
    ],
)
def test_cli():
    cli_args = RecordData.cli()
    assert cli_args["abbreviations"] == Path("abbreviations.txt")
    assert cli_args["start_log"] == Path("start.log")
    assert cli_args["stop_log"] == Path("end.log")
    assert cli_args["asc"]
    assert cli_args["driver"] == "SVF"
