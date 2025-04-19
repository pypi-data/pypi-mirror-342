# Snap Notify

A Python tool for sending notifications to Slack using a modular DSL template system. This tool allows you to define message templates in YAML format and send them to Slack channels with variable interpolation support.

## Features

- 📝 YAML-based message templates
- 🔄 Variable interpolation using Jinja2
- 🧵 Support for threaded messages
- 🎯 Simple CLI interface
- 🔒 Secure token management

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

Use the CLI to send your message:

```bash
snap-notify --file path/to/template.yaml
```

You can specify the template format using the `--format` or `-t` option:

```bash
snap-notify --file path/to/template.yaml --format yaml
# or using the short form
snap-notify -f path/to/template.yaml -t yaml
```

Currently supported formats:
- `yaml` (default): YAML template format

## Template Structure

The template supports the following fields:

- `channel`: The Slack channel to send the message to (required)
- `thread_ts`: Thread timestamp for threaded messages (optional)
- `blocks`: Array of Slack block elements
- `interpolate`: Dictionary of variables for template interpolation

## License

MIT License - see [LICENSE](LICENSE) for details.