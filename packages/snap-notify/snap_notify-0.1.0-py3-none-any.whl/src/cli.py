import click
from src import parser, core, slack_client

@click.command()
@click.option('--file', '-f', 'file_path', required=True, help='Path to the template file.')
@click.option('--format', '-t', 'file_type', default='yaml', help='Template format (yaml).')
def send(file_path, file_type):
    """
    Send a Slack message using a modular DSL template.
    """
    try:
        # Load and process the template
        template = parser.load_template(file_path, file_type)
        interpolated = parser.interpolate_template(template)
        payload = core.prepare_message(interpolated)
        
        # Send to Slack
        slack_client.send_message(payload)

    except Exception as e:
        click.echo(f"Error: {e}", err=True)


def main():
    send()
