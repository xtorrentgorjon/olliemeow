
from kubernetes import client, config

import threading
import requests
import datetime
from time import sleep

class kube_listener(threading.Thread):
    def __init__(self, event_message_template, current_namespace, slack_url, logger):
        threading.Thread.__init__(self)
        self.event_dict = {}
        config.load_incluster_config()
        self.v1 = client.CoreV1Api()
        self.event_message_template = event_message_template
        self.current_namespace = current_namespace
        self.slack_url = slack_url
        self.logger = logger
        ret = self.v1.list_namespaced_event(self.current_namespace)
        content = ""
        for i in ret.items:
            self.event_dict[i.metadata.name] = i

    def run(self):
        while True:
            ret = self.v1.list_namespaced_event(self.current_namespace)
            content = ""
            for i in ret.items:
                if i.metadata.name not in self.event_dict:
                    self.event_dict[i.metadata.name] = i
                    content += str(i.metadata.name.split(".")[0]+"\n"+i.involved_object.kind+" "+i.reason+" "+str(i.last_timestamp))+"\n-----------\n"
            current_time = str(datetime.datetime.now())
            if content != "":
                message = self.event_message_template % (self.current_namespace, content, current_time)
                r = requests.post(self.slack_url, data=message)
                self.logger.info("POST request result from slack: {} {}".format(r.status_code, r.reason))
                self.logger.debug("{}".format(content))
            sleep(30)

    def get_dictionary(self):
        event_list = []
        for item in self.event_dict:
            event = {}
            event["unique_id"] = item
            event["resource_name"] = self.event_dict[item].metadata.name.split(".")[0]
            event["resource_type"] = self.event_dict[item].involved_object.kind
            event["event_type"] = self.event_dict[item].reason
            event["date"] = self.event_dict[item].last_timestamp
            event_list.append(event)
        return event_list
