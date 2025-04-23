import json

import boto3
from botocore.exceptions import ClientError


class NotifyEmail:
    """Core NotifyEmail Class.
       Usage:

        Import sendnotifications
        messages = []
        messages.append("Test")
        messages.append("Test1")
        notify = NotifyEmail("Title - Testing card",messages,"vthelu")

        Parameters:
             title: str - Subject
             messages:str - Stack of messages
             recipient: str - Recepient Team Identifier

       Send Messages to subscribed email address"""
    __topic_name_ = "sendnotification-sharedlib-sns-notify-email-events"
    __topcic_arn_ = ""

    def __init__(self, title: str, message_body: str, recepient: str = None, message_attr: str = None) -> None:
        self.__topcic_arn_ = self.__get_topic_arn_(self.__topic_name_)
        self.__send_message_to_email_(title=title, message_body=message_body, recepient=recepient,
                                      message_attr=message_attr)

    def __send_message_to_email_(self, title: str, message_body: str, recepient: str = None,
                                 message_attr: str = None) -> None:
        client = boto3.client("sns")

        if not message_attr:
            message_attr = {'Team': {'StringValue': recepient, 'DataType': 'String'}}
        response = client.publish(TargetArn=self.__topcic_arn_, Message=json.dumps(message_body), Subject=title,
                                  MessageAttributes=message_attr)
        print(response)

    def __get_topic_arn_(self, topic_name: str):
        sns_client = boto3.client('sns')
        sts_client = boto3.client('sts')

        try:
            caller_identity = sts_client.get_caller_identity()
            account_id = caller_identity['Account']
            response = sns_client.get_topic_attributes(
                TopicArn=f"arn:aws:sns:{sns_client.meta.region_name}:{account_id}:{topic_name}")
            return response['Attributes']['TopicArn']
        except ClientError as e:
            if e.response['Error']['Code'] == 'NotFoundException':
                return None
            else:
                raise e

# def main():
#     messages = []
#     messages.append("New adaptive card")
#     messages.append("New method of message on teams channel")
#
#     notify = NotifyEmail("Title - Testing card",messages,"vthelu")
#
# if __name__ == "__main__":
#     main()
