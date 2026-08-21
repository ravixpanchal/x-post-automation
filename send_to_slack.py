import os
import sys
import requests

# Load environment variables from local .env file if present
env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(env_file):
    with open(env_file, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "https://hooks.slack.com/services/YOUR/WEBHOOK/URL")

def send_tweet_to_slack(tweet):
    message = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Generated Tweet:*\n\n{tweet}"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Approve ✅",
                            "emoji": True
                        },
                        "style": "primary",
                        "value": tweet,
                        "action_id": "approve"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Reject ❌",
                            "emoji": True
                        },
                        "style": "danger",
                        "value": "rejected",
                        "action_id": "reject"
                    }
                ]
            }
        ]
    }
    response = requests.post(WEBHOOK_URL, json=message)
    print("Slack Response:", response.status_code, response.text)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        send_tweet_to_slack(sys.argv[1])
    else:
        print("Usage: python send_to_slack.py <tweet_text>")