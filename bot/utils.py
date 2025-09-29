import os

import psutil
import requests

critical_level = 90.0


def alert(text):
    data_for_request = {}
    data_for_request["url"] = (
        f'https://api.telegram.org/{os.getenv("TG_KEY")}/sendMessage'
    )
    data_for_request["data"] = {
        "chat_id": os.getenv("TG_CHAT"),
        "text": text,
    }
    res = requests.post(**data_for_request)


if psutil.virtual_memory().percent > critical_level:
    alert(f"🆘 RAM is over 90% 🆘 {psutil.virtual_memory().percent} 🆘")

if psutil.cpu_percent(interval=1) > critical_level:
    alert(f"🆘 CPU is over 90% 🆘 {psutil.cpu_percent(interval=1)} 🆘")

if psutil.disk_usage("/").percent > critical_level:
    alert(f'🆘 HDD is over 90% 🆘 {psutil.disk_usage("/").percent} 🆘')
