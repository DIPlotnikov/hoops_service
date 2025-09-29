import os
from datetime import datetime
from os import path
from pathlib import Path

from django.core.management import call_command


def backup_data():
    try:
        output_path = (
            f'{path.join(Path(__file__).resolve().parent.parent, "backup", str(int(datetime.now().timestamp())))}.json'
        )
        call_command(f"dumpdata --exclude auth.permission --exclude contenttypes --output {output_path}")
        print(path)

        command = f'curl -v -F "chat_id={os.getenv("TG_CHAT")}" -F document=@{output_path} https://api.telegram.org/{os.getenv("TG_KEY")}/sendDocument'
        os.system(command)

    except Exception as e:
        print(e)
        with open("/var/www/log.log", "w", encoding="utf-8") as file:
            file.write(str(e))


if __name__ == "__main__":
    backup_data()
