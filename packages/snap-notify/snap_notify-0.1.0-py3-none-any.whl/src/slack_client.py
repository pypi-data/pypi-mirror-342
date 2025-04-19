from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os

def get_slack_client():
    """
    Initializes and returns a Slack WebClient using the SLACK_BOT_TOKEN env variable.
    """
    token = os.getenv("SLACK_BOT_TOKEN")
    if not token:
        raise EnvironmentError("SLACK_BOT_TOKEN environment variable is not set.")
    return WebClient(token=token)


def send_message(payload: dict):
    """
    Sends a message to Slack using the provided payload.

    Args:
        payload (dict): Slack message payload.
    """
    client = get_slack_client()

    try:
        response = client.chat_postMessage(**payload)
        print(f"Message sent successfully. TS: {response['ts']}")
        return response
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")
        raise
