# evlog

This is a little utility I use for logging my daily activities and events. It is written in Python.

## Install

```bash
pipx install evlog
```

## Usage

To change the directory where evlogs are stored, set a shell environment variable EVLOG_DIR. To make this change permament, set the following in your shell configuration:

```bash
export EVLOG_DIR="/path/to/evlog/dir"
```

Otherwise, the default evlog directory will be `~/evlogs`.

To get started, add your first evlog entry! This will create a JSON file under your evlog directory for the day and ensure the evlog directory exists. E.g.:

```bash
evlog add -m "Started new evlog. Yay!"
```

```bash
usage: evlog [-h] [-v] {add,edit,rm,ls,lsfiles,search} ...

positional arguments:
  {add,edit,rm,ls,lsfiles,search}

options:
  -h, --help            show this help message and exit
  -v, --version         Print version information
```

### Example list output
![screenshot.png](/screenshot.png)

