# Snap Notify

A Python tool for sending notifications to Slack using a modular DSL template system. This tool allows you to define message templates in YAML format and send them to Slack channels with variable interpolation support.

## Features

- YAML-based message templates
- Variable interpolation using Jinja2
- Support for threaded messages
- Simple CLI interface
- Secure token management
- Programmatic usage with Python API

## Installation

```bash
pip install snap-notify
```

## Prerequisites

- Python 3.13 or higher
- A Slack Bot Token (set as `SLACK_BOT_TOKEN` environment variable)

## Usage

### 1. Create a Message Template

Create a YAML file with your message template. Example:

```yaml
channel: "#your-channel"
blocks:
  - type: "section"
    text: "Hello {{ name }}! Here's your daily update:"
  - type: "context"
    elements:
      - type: "mrkdwn"
        text: "Report generated at {{ timestamp }}"
interpolate:
  name: "John"
  timestamp: "2024-03-20 10:00:00"
```

### 2. Send the Message

#### Using the CLI

```bash
snap-notify --file path/to/template.yaml
```

You can specify the template format using the `--format` or `-t` option:

```bash
snap-notify --file path/to/template.yaml --format yaml
# or using the short form
snap-notify -f path/to/template.yaml -t yaml
```

#### Using the Client API

```python
from snap_notify import Slack
from snap_notify.parser import parse_template

# Initialize the Slack client
slack = Slack()  # Uses SLACK_BOT_TOKEN from environment
# Or provide token directly
# slack = Slack(token="your-slack-token")

# Method 1: Parse from a file
template = parse_template("path/to/template.yaml")

# Method 2: Import a template from your project
from your_project.templates import daily_update
template = parse_template(daily_update)

# Method 3: Define template in code
template = {
    "channel": "#your-channel",
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Hello {{ name }}! Here's your daily update:"
            }
        }
    ],
    "interpolate": {
        "name": "John"
    }
}

# Send the message
response = slack.send_message(template)
```

You can also create message payloads programmatically:

```python
from snap_notify import Slack

slack = Slack()

# Create a message payload
payload = {
    "channel": "#your-channel",
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Hello from Python!"
            }
        }
    ]
}

# Send the message
response = slack.send_message(payload)
```

#### Working with Threads

You can create threaded conversations by using the `thread_ts` parameter:

```python
from snap_notify import Slack

slack = Slack()

# Create a parent message
parent_message = {
    "channel": "#your-channel",
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "This is the parent message"
            }
        }
    ]
}

# Send the parent message and get its timestamp
parent_response = slack.send_message(parent_message)
thread_ts = parent_response["ts"]

# Create a child message in the thread
child_message = {
    "channel": "#your-channel",
    "thread_ts": thread_ts,  # Link to parent message
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "This is a reply in the thread"
            }
        }
    ]
}

# Send the child message
slack.send_message(child_message)
```

You can also use templates with threads:

```yaml
# parent.yaml
channel: "#your-channel"
blocks:
  - type: "section"
    text: "Parent message with {{ variable }}"
interpolate:
  variable: "interpolated value"

# child.yaml
channel: "#your-channel"
thread_ts: "{{ parent_ts }}"  # Will be replaced with actual timestamp
blocks:
  - type: "section"
    text: "Child message in thread"
interpolate:
  parent_ts: "1234567890.123456"  # Replace with actual parent message timestamp
```

Currently supported formats:
- `yaml` (default): YAML template format

## Template Structure

The template supports the following fields:

- `channel`: The Slack channel to send the message to (required)
- `thread_ts`: Thread timestamp for threaded messages (optional)
- `blocks`: Array of Slack block elements
- `interpolate`: Dictionary of variables for template interpolation

## Environment Variables

- `SLACK_BOT_TOKEN`: Your Slack Bot User OAuth Token (required)

## License

MIT License - see [LICENSE](LICENSE) for details.