#####
import logging
import os
import datetime


### Logging parameters

LOGGER = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)
LOGGER.setLevel(logging.INFO)

### Slack api URL

SLACK_URL = os.environ['SLACK_URL']

### Kubernetes parameters

CURRENT_NAMESPACE = "default"
with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace") as namespace_file:
    CURRENT_NAMESPACE = namespace_file.read().strip()

### Message format templates

STARTUP_INFORMATION_MESSAGE = """{
        "attachments": [
            {
                "color": "#fc7f03",
                "title": ":information_source: Olliemeow Reporting System starting up in namespace %s.",
                "footer": "Olliemeow reporting system :page_with_curl::cat2:",
                "ts": "%s"
            }
        ]
    }"""


EVENT_MESSAGE_TEMPLATE = '''{ "attachments": [
        {
            "color": "#fc7f03",
            "title": "New events in namespace %s.",
            "text": "%s",
            "footer": "Olliemeow reporting system :page_with_curl::cat2:",
            "ts": "%s"
        }
    ]
}'''
