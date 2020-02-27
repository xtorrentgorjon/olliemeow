from config.config import STARTUP_INFORMATION_MESSAGE, EVENT_MESSAGE_TEMPLATE, LOGGER, SLACK_URL, CURRENT_NAMESPACE
from kube_listener.kube_listener import kube_listener
from flask import Flask, request, jsonify
import requests
import datetime


kl = kube_listener(EVENT_MESSAGE_TEMPLATE, CURRENT_NAMESPACE, SLACK_URL, LOGGER)

app = Flask(__name__)
app.debug = True

@app.route('/api/v1/events/<type>', methods=['GET'])
def api_get_events_json(type):
    if request.method == 'GET':
        if type == 'json':
            event_table = kl.get_dictionary()
            return jsonify(event_table)
        else:
            return ("Method not supported.", 400)


startup_time = str(datetime.datetime.now())
LOGGER.info("{}".format(STARTUP_INFORMATION_MESSAGE))
startup_information_message = STARTUP_INFORMATION_MESSAGE % (CURRENT_NAMESPACE, startup_time)
r = requests.post(SLACK_URL, data=startup_information_message)
LOGGER.info("POST request result from slack: {} {}".format(r.status_code, r.reason))

if __name__ == "__main__":
    kl.start()
    app.run(host="0.0.0.0", port=5000)
    kl.join()
