import logging

from pathlib import Path

from .driver_3_version import RecordData


def main():
    logging.basicConfig(level=logging.INFO)

    folder = Path(__file__).parent / "data"

    if not folder.exists():
        logging.critical(f"Folder not found: {folder}, creating it now...")
        folder.mkdir(parents=True, exist_ok=True)

    try:
        cli_args = RecordData.cli()

        record = RecordData()

        good_records, bad_records = record.build_report(
            folder=folder,
            file=cli_args["abbreviations"],
            start_file=cli_args["start_log"],
            stop_file=cli_args["stop_log"],
            asc=cli_args["asc"],
            driver=cli_args["driver"],
        )

        RecordData.print_report(good_records, bad_records)

    except FileNotFoundError as e:
        logging.error(f"Critical error: {e}")


if __name__ == "__main__":
    main()
