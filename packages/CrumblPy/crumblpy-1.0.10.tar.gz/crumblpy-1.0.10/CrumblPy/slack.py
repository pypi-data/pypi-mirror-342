import os
from prefect.blocks.system import Secret
from slack_sdk import WebClient

class SlackToolKit:
    def __init__(self, prefect=False, token=None, default_channel='U04RAQM788L'):
        if token:
            # If token is provided as input, use it
            self.token = token
        elif prefect:
            # if `prefect` is True, load token from Prefect secrets
            self.token = Secret.load("prefect-slack-token").get() 
        else:
            self.token = os.environ['SLACK_TOKEN']
            
        self.client = WebClient(token=self.token)
        self.default_channel = default_channel

    def post_message(self, message=None, channel=None, thread_id=None, blocks=None):
        """
        Use the official Slack Block Kit Builder to create blocks:
        https://app.slack.com/block-kit-builder/
        """
        if channel is None:
            channel = self.default_channel
        self.client.chat_postMessage(channel=channel, thread_ts=thread_id, text=message, blocks=blocks)

    def post_file(self, file_path, message, channel=None,thread_id=None):
        if channel is None:
            channel = self.default_channel
        self.client.files_upload(
                channels=channel,
                file=file_path,
                title=file_path,
                initial_comment=message,
                thread_ts=thread_id
            )
        os.remove(file_path)

    def get_thread_id(self, channel):
        response = self.client.conversations_history(channel=channel)
        return response['messages'][0]['ts']


    def push_notification(self, project=None, channel=None, e=None):

        if e:
            message = f"An error occurred for {project}:\n{e}"
        else:
            message = f"Successfully completed the task for {project}."

        self.post_message(message, channel)