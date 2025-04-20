#!/usr/bin/env python3

import argparse
import datetime as dt
import json
import os
import sys
import time
from pathlib import Path

import jsonschema
from jsonschema import validate
from rich import box
from rich.console import Console
from rich.table import Table
from rich.traceback import install

install(show_locals=True)

VERSION = "0.1.7"

default_date = dt.date.today().strftime("%Y-%m-%d")
EVLOG_DIR = os.getenv("EVLOG_DIR")
if EVLOG_DIR is None:
    evlog_dir = Path("~/evlogs").expanduser()
else:
    evlog_dir = Path(EVLOG_DIR)


def evlog_init(filename):
    """Initialize evlog file and directory, if necessary.

    evlog_dir is taken from the current shell's EVLOG_DIR environment variable, or else it defaults to
    ~/evlogs.
    """
    evlog_file = evlog_dir.joinpath(filename).with_suffix(".json")

    evlog_dir.mkdir(exist_ok=True)
    evlog_file.touch()

    json_array = []

    with open(evlog_file, "w") as ef:
        json.dump(json_array, ef)


def evlog_list(args):
    """List evlog entries.

    Lists evlog entries for provided timestamp range and/or evlog file
    """
    if args.file:
        selected_evlog_file = evlog_dir.joinpath(args.file)
    else:
        selected_evlog_file = evlog_dir.joinpath(default_date + "_evlog").with_suffix(
            ".json"
        )

    if not selected_evlog_file.exists():
        exit("evlog file %s not found. Are you sure it exists?" % selected_evlog_file)

    if not args.start:
        ts_from = selected_evlog_file.stem[:10] + " 00:00:00"
    else:
        dt.datetime.strptime(args.start, "%Y-%m-%d %H:%M:%S")
        ts_from = args.start

    if not args.end:
        ts_to = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        dt.datetime.strptime(args.end, "%Y-%m-%d %H:%M:%S")
        ts_to = args.end

    with open(selected_evlog_file, "r") as ef:
        json_data = json.load(ef)

    table = Table(style="#5f00ff", header_style="bold", box=box.ROUNDED)
    table.add_column("Index", justify="right", style="white")
    table.add_column("Timestamp", justify="left", style="#ff87d7")
    table.add_column("Message", justify="left")

    for i in range(len(json_data)):
        if json_data[i]["timestamp"] > ts_from and json_data[i]["timestamp"] < ts_to:
            table.add_row(str(i), json_data[i]["timestamp"], json_data[i]["message"])

    console = Console(color_system="256")
    console.print(table)


def evlog_list_files(args):
    """List all evlog files.

    Lists all evlog files currently present in evlog directory.
    """
    for file in sorted(evlog_dir.iterdir()):
        if file.is_file():
            if args.absolute:
                print(file)
            else:
                print(file.name)


def evlog_search(args):
    """Search for a string.

    Searches all evlog files and prints found matches.
    """
    found_entries = list()
    evlog_list = [file.name for file in evlog_dir.iterdir()]

    console = Console()

    for file in evlog_list:
        with open(evlog_dir.joinpath(file), "r") as ef:
            json_data = json.load(ef)
            for entry in json_data:
                if args.word in entry["message"]:
                    found_entries.append(entry)

    if found_entries:
        for entry in found_entries:
            console.print(
                "[bold green]{0}[/bold green] {1}".format(
                    entry["timestamp"], entry["message"]
                )
            )
    else:
        console.print(
            "[bold yellow]{0}[/bold yellow] was not found in any of the evlog files".format(
                args.word
            )
        )


def evlog_sort(file):
    """Sort evlog entries.

    Entries are sorted by provided timestamp.
    """
    with open(file, "r") as ef:
        json_data = json.load(ef)
        json_data.sort(
            key=lambda x: time.mktime(
                time.strptime(x["timestamp"], "%Y-%m-%d %H:%M:%S")
            )
        )

    with open(file, "w") as ef:
        json.dump(json_data, ef, indent=4)


def validate_json(file):
    """Validate JSON data.

    Call jsonschema.validate on `file`.
    """
    evlog_schema = {
        "type": "array",
        "properties": {
            "timestamp": {"type": "string"},
            "message": {"type": "string"},
        },
    }

    with open(file, "r") as ef:
        json_data = json.load(ef)

    try:
        validate(instance=json_data, schema=evlog_schema)
    except jsonschema.ValidationError as err:
        print("Invalid JSON detected on %s" % file)
        print(err)


def evlog_append(args):
    """
    Append a new evlog entry to the evlog file.

    Use evlog file indicated by provided timestamp, or else use the evlog file for current day.
    """
    if not args.timestamp:
        ts = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        dt.datetime.strptime(args.timestamp, "%Y-%m-%d %H:%M:%S")
        ts = args.timestamp

    evlog_filename = ts[:10] + "_evlog"
    evlog_file = evlog_dir.joinpath(evlog_filename).with_suffix(".json")

    if not evlog_file.exists():
        evlog_init(evlog_file)

    entry = {"timestamp": ts, "message": args.message}

    with open(evlog_file, "r+") as ef:
        json_data = json.load(ef)
        json_data.append(entry)
        ef.seek(0)
        json.dump(json_data, ef, indent=4)

    evlog_sort(evlog_file)
    validate_json(evlog_file)


def evlog_edit(args):
    """Edit evlog entry at provided index argument."""
    if args.file:
        evlog_file = evlog_dir.joinpath(args.file)
    else:
        evlog_file = evlog_dir.joinpath(default_date + "_evlog").with_suffix(".json")

    if not evlog_file.exists():
        exit(
            "evlog file not found. Please run 'evlog append' to start a new evlog file."
        )

    with open(evlog_file, "r+") as ef:
        json_data = json.load(ef)
        json_data[args.index]["message"] = args.message
        ef.seek(0)
        json.dump(json_data, ef, indent=4)

    validate_json(evlog_file)


def evlog_remove(args):
    """Remove an evlog entry at provided index argument."""
    if args.file:
        evlog_file = evlog_dir.joinpath(args.file)
    else:
        evlog_file = evlog_dir.joinpath(default_date + "_evlog").with_suffix(".json")

    if not evlog_file.exists():
        exit(
            "evlog file not found. Please run 'evlog append' to start a new evlog file."
        )

    with open(evlog_file, "r") as ef:
        json_data = json.load(ef)
        json_data.pop(args.index)

    with open(evlog_file, "w") as ef:
        json.dump(json_data, ef, indent=4)

    validate_json(evlog_file)


parser = argparse.ArgumentParser(prog="evlog")
parser.add_argument(
    "-v",
    "--version",
    action="version",
    version="%(prog)s {}".format(VERSION),
    help="Print version information",
)
subparsers = parser.add_subparsers()

add_parser = subparsers.add_parser("add", description="Add an evlog entry")
add_parser.add_argument(
    "-t",
    "--timestamp",
    required=False,
    type=str,
    action="store",
    help="Timestamp for evlog entry: str",
)
add_parser.add_argument(
    "-m",
    "--message",
    required=True,
    type=str,
    action="store",
    help="Message for evlog entry: str",
)
add_parser.set_defaults(func=evlog_append)

edit_parser = subparsers.add_parser("edit", description="Edit an evlog entry")
edit_parser.add_argument(
    "-i",
    "--index",
    required=True,
    type=int,
    action="store",
    help="Index of evlog entry: int",
)
edit_parser.add_argument(
    "-m",
    "--message",
    required=True,
    type=str,
    action="store",
    help="New message for evlog entry: str",
)
edit_parser.add_argument(
    "-f",
    "--file",
    required=False,
    type=str,
    action="store",
    help="evlog file to edit. Ex: 2022-10-02_evlog.json",
)
edit_parser.set_defaults(func=evlog_edit)

rm_parser = subparsers.add_parser("rm", description="Remove an evlog entry")
rm_parser.add_argument(
    "-i",
    "--index",
    required=True,
    type=int,
    action="store",
    help="Index of evlog entry: int",
)
rm_parser.add_argument(
    "-f",
    "--file",
    required=False,
    type=str,
    action="store",
    help="evlog file to remove from. Ex: 2022-10-02_evlog.json",
)
rm_parser.set_defaults(func=evlog_remove)

ls_parser = subparsers.add_parser("ls", description="List evlog entries")
ls_parser.add_argument(
    "-s",
    "--start",
    metavar="TIMESTAMP",
    required=False,
    type=str,
    action="store",
    help="From timestamp: str. Default is today at 00:00:00. Ex. 2022-09-28 13:45:00",
)
ls_parser.add_argument(
    "-e",
    "--end",
    metavar="TIMESTAMP",
    required=False,
    type=str,
    action="store",
    help="To timestamp: str. Default is today at now. Ex. 2022-09-28 21:00:00",
)
ls_parser.add_argument(
    "-f",
    "--file",
    required=False,
    type=str,
    action="store",
    help="evlog file to view. Ex: 2022-10-02_evlog.json",
)
ls_parser.set_defaults(func=evlog_list)

ls_files_parser = subparsers.add_parser("lsfiles", description="List all evlog files")
ls_files_parser.add_argument(
    "-a",
    "--absolute",
    required=False,
    action="store_true",
    help="List the absolute paths of the evlog files",
)
ls_files_parser.set_defaults(func=evlog_list_files)

search_parser = subparsers.add_parser(
    "search", description="Search for keywords in evlog files"
)
search_parser.add_argument(
    "-w", "--word", required=True, type=str, action="store", help="Word to search for"
)
search_parser.set_defaults(func=evlog_search)


def main():
    """Parse command line arguments and run desired function.

    Checks if the number of arguments provided at the command line is less than the required number,
    and if so, it prints the usage message.
    """
    if len(sys.argv) < 2:
        parser.print_usage()
    else:
        args = parser.parse_args()
        args.func(args)


if __name__ == "__main__":
    main()
