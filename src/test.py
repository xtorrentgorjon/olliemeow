import datetime
import requests

#title = "Olliemeow Reporting System"
#text = ":information_source: Olliemeow Reporting System starting up"
#notification_color = "#fc7f03"
#current_time = str(datetime.datetime.now())

information = '''{ "attachments": [
            {
                "color": "#fc7f03",
                "title": ":information_source: Olliemeow Reporting System starting up",
                "footer": ":cat: :page_with_curl: Olliemeow reporting system",
                "ts": {}
            }
        ]
	}
'''

r = requests.post("https://hooks.slack.com/services/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", data=information)

print(r.status_code, r.reason)
