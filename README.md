# Random coffee slack bot
Takes a random user from the Slack user lists and forces them to get coffee :)

###
##Install docker
https://docs.docker.com/install/

## Slack
1) Create a Slack app
https://api.slack.com/apps?new_app=1

2) Install the app

3) Create a bot user

4) Invite your bot user to a channel

5) Update the code (my_script.py) with your tokens / client

## Run
### Build docker image
docker build --force-rm -t slackbot .

### Docker run
docker run -it --rm --name slackbot slackbot

### Usage
1) Go to the Slack channel with the coffee bot
2) Type: @<name_of_bot_user> I want coffee
3) Random user from slack group is tagged