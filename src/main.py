from kubernetes import client, config
from time import sleep

import datetime
import requests
import logging
import os

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

slack_url = os.environ['SLACK_URL']

current_namespace = "default"
with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace") as namespace_file:
    current_namespace = namespace_file.read().strip()

startup_time = str(datetime.datetime.now())

startup_information = """{
        "attachments": [
            {
                "color": "#fc7f03",
                "title": ":information_source: Olliemeow Reporting System starting up in namespace %s.",
                "footer": "Olliemeow reporting system :page_with_curl::cat2:",
                "ts": "%s"
            }
        ]
    }""" % (current_namespace, startup_time)


event_message = '''{ "attachments": [
        {
            "color": "#fc7f03",
            "title": "New events in namespace %s.",
            "text": "%s",
            "footer": "Olliemeow reporting system :page_with_curl::cat2:",
            "ts": "%s"
        }
    ]
}'''

config.load_incluster_config()
v1 = client.CoreV1Api()

try:
    print("Listing pods with their IPs:")
    ret = v1.list_namespaced_pod(current_namespace)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
except Exception as e:
    print(e)

#title = "Olliemeow Reporting System"
#text = ":information_source: Olliemeow Reporting System starting up"
#notification_color = "#fc7f03"

logger.info("{}".format(startup_information))
r = requests.post(slack_url, data=startup_information)
logger.info("POST request result from slack: {} {}".format(r.status_code, r.reason))

# init the dictionary
event_dict = {}
ret = v1.list_namespaced_event(current_namespace)
content = ""
for i in ret.items:
    event_dict[i.metadata.name] = i

while True:
    ret = v1.list_namespaced_event(current_namespace)
    content = ""
    for i in ret.items:
        if i.metadata.name not in event_dict:
            event_dict[i.metadata.name] = i
            content += str(i.metadata.name.split(".")[0]+"\n"+i.involved_object.kind+" "+i.reason+" "+str(i.last_timestamp))+"\n-----------\n"
    current_time = str(datetime.datetime.now())
    if content != "":
        r = requests.post(slack_url, data=event_message % (current_namespace, content, current_time))
        logger.info("POST request result from slack: {} {}".format(r.status_code, r.reason))
        logger.debug("{}".format(content))
    sleep(30)
