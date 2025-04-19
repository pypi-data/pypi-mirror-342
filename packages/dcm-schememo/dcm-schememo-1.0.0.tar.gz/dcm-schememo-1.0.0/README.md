# dcm-schememo

[日本語](README.ja.md)

A Python library for parsing memo data from VCS files exported by docomo Schedule & Memo App.

## Installation

```bash
pip install dcm-schememo
```

## Usage

### Basic Usage

```python
from dcm_schememo import parse_vcs_file

# Parse VCS file
events = parse_vcs_file("path/to/your.vcs")

# Check event contents
for event in events:
    print(f"Title: {event.summary}")
    print(f"Description: {event.description}")
    print(f"Type: {event.type}")  # NOTE or TASK
    print(f"Last Modified: {event.last_modified}")
```

### Available Fields

The `Note` class has the following fields:

- `type`: Note type ('NOTE', 'SHOPPING', 'TODO', 'TODOEVENT', etc.)
- `summary`: Title
- `description`: Description text
- `last_modified`: Last modified datetime (datetime type with timezone)
- `photo`: Image data (bytes)
- `tz`: Timezone (e.g., "+09:00")
- `decosuke`: Decoration emoji data (bytes, typically GIF image)
- `aalarm`: Alarm time (datetime type with timezone)
- `status`: Task status (e.g., "NEEDS-ACTION")
- `due`: Task due date (datetime type with timezone)
- `location`: Location
- `show`: Display setting (True/False/None)

## Examples

The `examples` directory contains the following sample code:

### Google Keep Integration Sample (google_keep.py)

A sample that reads notes from VCS files and saves them to Google Keep. It implements the following features:

- Google account login process
- Reading notes from VCS files
- Saving note titles and content to Google Keep
- Saving attached images as temporary files

## License

MIT License
