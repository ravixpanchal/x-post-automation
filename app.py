from flask import Flask, request
import json
from post_to_x import post_to_x

app = Flask(__name__)


@app.route("/slack/actions", methods=["POST"])
def slack_actions():

    payload = json.loads(request.form["payload"])

    action = payload["actions"][0]
    tweet = action["value"]

    if action["action_id"] == "approve":

        print("APPROVED")
        print(tweet)

        # Run in a background thread to avoid Slack webhook timeout
        import threading
        threading.Thread(target=post_to_x, args=(tweet,)).start()

    elif action["action_id"] == "reject":

        print("REJECTED")

    return ""


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )