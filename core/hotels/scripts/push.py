import json

import requests


def send_push(fcm_token, text):
    server_key = "AAAA-Zg-5K8:APA91bEwAQIf-5EAsYAUaqnEoVtA41XvulEzHrOcUNcWroOyzf2bVbnLMpLr8MCgSqUky81RFrCxUHtdu_Qpfva0h4ZydZGVeNzST5Unuh30qwAA4rB0wrN15cqrfV5kcjNO1FeQ7XOS"
    url = "https://fcm.googleapis.com/fcm/send"

    headers = {"Authorization": f"key={server_key}", "Content-Type": "application/json"}

    data_push = {"to": fcm_token, "notification": {"title": "HOOPS Service", "body": text}}
    requests.post(url, data=json.dumps(data_push), headers=headers)
