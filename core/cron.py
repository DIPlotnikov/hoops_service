from datetime import datetime
from django.core.management import call_command
from os import path
from pathlib import Path

def backup_data():
    try:
        #call_command('dbbackup')
        f = open(f'{path.join(  Path(__file__).resolve().parent.parent, "backup",str(int(datetime.now().timestamp())))}.json', 'w', encoding='windows-1251')
        call_command('dumpdata',  stdout=f)
        f.close()

    except Exception as e:
        with open('/var/www/log.log', 'w', encoding='utf-8') as file:
            file.write(str(e))




if __name__=='__main__':
    backup_data()
