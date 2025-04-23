import http.client
import json

import urllib3

from .channels import NotifyChannels as nc


class NotifyMsTeams:
    """Core NotifyMSTeam Class.
    Usage:

     from
     messages = []
     messages.append("Test")
     messages.append("Test1")
     notify = NotifyMsTeams("homes-analytics-alerts",messages,"Test Title",1,"warn")

     Parameters:
          channel: str - Channel name
          messages:str - Stack of messages
          header_text: str - Title / Subject
          messagetype:str - 0 - Direct Mesage , 1 - Adapative Card (default)
          color:str = "good" - Alert Type , good , warn, attn

         e.g "dba-only",messages,"Test Title",1,"warn"
             "dba-only",messages,"Test Title"

    Send Messages to webhook url"""
    __idx_ = 1
    __channel_ = "dba-test-notifications"

    __webhook_mapper_ = {
        0: {"workflow_name": "informational direct message workflow",
            "message_type": "Direct Message",
            "webhook": nc.webhook[__channel_]},
        1: {"workflow_name": "informational adaptive card",
            "message_type": "Preformed Adaptive Card",
            "webhook": nc.webhook[__channel_]},
    }

    __workflow_name_ = __webhook_mapper_[__idx_]["workflow_name"]
    __message_type_ = __webhook_mapper_[__idx_]["message_type"]
    __webhook_ = __webhook_mapper_[__idx_]["webhook"]
    __header_ = f""
    __message_ = ""

    def __init__(self, channel: str = "dba-test-notifications", messages: list[str] = [], header: str = None,
                 color: str = "good",
                 messagetype: str = 1) -> None:
        """Construct webhook object.:
        Args:
                channel: Teams webhook URL to send all cards (messages) to.
                messagetype: 0 - "driect message" / 1 - "adaptive card"
                color: "good" / "attention" / "warning"

        Returns:
                None.

        Raises:
                None.
        """
        message = ""
        self.__channel_ = channel
        self.__message_ = messages
        self.__header_ = header
        self.__idx_ = messagetype
        self.__webhook_ = nc.webhook[channel]
        if messagetype == 0:
            print("Direct message")
            if color == "good":
                color = "2DC72D"
            elif color == "warn":
                color = "f6b26b"
            elif color == "attn":
                color = "e06666"
            for msg in messages:
                message = message + msg + '<br>'
            response = self.__send_message_to_ms_teams_(self.__webhook_, header, message, color)

        elif messagetype == 1:
            print("Preformed adaptive card")

            if color == "warn":
                color = "warning"
            elif color == "attn":
                color = "attention"
            else:
                color = "good"
            for msg in messages:
                msg = msg.replace("<br>", "\n\n")
                message = message + msg + '\n\n'
            webhook = self.__webhook_['uri']
            adaptive_card = self.__create_adaptive_card_(header, message, color)
            response = self.__send_adaptive_card_to_ms_teams_(webhook, adaptive_card)
        print(response)

    def __create_adaptive_card_(self, header: str, message_body: str, color: str = "good") -> dict[
        str, str | list[dict[str, str | bool] | dict[str, str | bool]]]:
        try:

            '''
            create and return an adaptive card
            '''
            adaptive_card = {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.2",
                "body": [
                    {
                        "type": "TextBlock",
                        "text": header,
                        "style": "heading",
                        "size": "Large",
                        "weight": "bolder",
                        "wrap": True,
                        "width" "auto"
                        "color": color
                    },
                    {
                        "type": "TextBlock",
                        "weight": "default",
                        "wrap": True,
                        "width" "auto"
                        "size": "default",
                        "text": message_body
                    },
                ]
            }
            self.header_text = header
            self.message = message_body
            return adaptive_card
        except:
            return None

    def __send_adaptive_card_to_ms_teams_(self, webhook: str, adaptive_card: dict[
        str, str | list[dict[str, str | bool] | dict[str, str | bool]]]) -> http.client.responses:
        try:
            '''
            send an adaptive card to an MS Teams channel using a webhook
            '''
            http = urllib3.PoolManager()
            payload = json.dumps(
                {
                    "type": "message",
                    "attachments": [
                        {"contentType": "application/vnd.microsoft.card.adaptive", "content": adaptive_card}]
                }
            )
            headers = {"Content-Type": "application/json"}
            response = http.request("POST", webhook, body=payload, headers=headers)
            print("response status:", response.status)
            return response
            if response.status >= 300:
                print(response)

        except:
            print('Status Code: {}'.format(response.status_code))
            print('Response: {}'.format(response.content))

    def __send_message_to_ms_teams_(self, webhook, title: str, message_body: str,
                                    theme: str = "2DC72D") -> http.client.responses:
        try:

            '''
            send a simple text message to an MS Teams channel using a webhook
    
            The webhook receives a simple message,
            the Power Automate workflow creates an adaptive card and posts to MS Teams
            Ensure that the Power Automate workflow has been so configured.
            '''
            http = urllib3.PoolManager()
            payload = json.dumps(
                {
                    "@context": "http://schema.org/extensions",
                    "type": "MessageCard",
                    "title": title,
                    "summary": "This workflow accepts a direct message rather than a preformed adaptive card",
                    "text": message_body,
                    "themeColor": theme
                }
            )
            headers = {"Content-Type": "application/json"}
            response = http.request("POST", webhook, body=payload, headers=headers)
            return response
            print("response status:", response.status)
            if response.status >= 300:
                print(response)

        except:
            print('Status Code: {}'.format(response.status_code))
            print('Response: {}'.format(response.content))

# def main():
#     messages = []
#     messages.append("New adaptive card")
#     messages.append("New method of message on teams channel")
#     notify = NotifyMsTeams("dba-only",messages,"Title - Testing card")
#
# if __name__ == "__main__":
#     main()
