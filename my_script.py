import os
import time
import re
import json
import random
from slackclient import SlackClient

# instantiate Slack client
client_id = "" # The ClientID of your app
bot_user_access_token = "" # The OAuth token of your bot user

slack_client = SlackClient(bot_user_access_token)

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
COFFEE_EXAMPLE = "I want coffee"
BEER_EXAMPLE = 'I want beer'
TOSTI_DU_CHEF_EXAMPLE = 'I want a tosti du chef'
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == client_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Options: *{}*.".format([COFFEE_EXAMPLE, BEER_EXAMPLE, TOSTI_DU_CHEF_EXAMPLE])

    # Finds and executes the given command, filling in response
    response = None

    # This is where you start to implement more commands!
    if command == COFFEE_EXAMPLE or command == BEER_EXAMPLE or command == TOSTI_DU_CHEF_EXAMPLE:
        userListDict = slack_client.api_call(
            "users.list",
            channel=channel
        )

        usernames = []

        members = userListDict["members"]

        for value in members:
            if not value["deleted"] and not value["is_bot"] and value["name"] != "slackbot":
                usernames.append(value["name"])
        
        user = random.choice(usernames)

        response = '@' + user

    if command == COFFEE_EXAMPLE:
    	response += ' go get the team coffee!'

    if command == BEER_EXAMPLE:
    	response += ' go get the team beer :)'

    if command == TOSTI_DU_CHEF_EXAMPLE:
    	response += ' reserve @ Kandinsky (0416 563 622)'

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        link_names=1,
        channel=channel,
        text=response or default_response
    )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        client_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")