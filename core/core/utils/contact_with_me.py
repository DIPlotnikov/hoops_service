import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

recievers = ["z.palelashvili@hoopswork.com", "a.schetinina@hoopswork.com"]


@csrf_exempt
def contact_with_me(request):
    try:
        if request.method not in ["PUT", "POST"]:
            return HttpResponse(status=500)
        body = json.loads(request.body.decode("utf-8"))
        text = body.get("text", "")
        fromaddr = "registr@hoopswork.com"
        mypass = "NSrRa4DtgwvV6crpVSuF"

        msg = MIMEMultipart()
        msg["From"] = f"HOOPS <{fromaddr}>"
        msg["Subject"] = "Свяжитесь со мной!"

        body = f"Привет! Новое обращение с лендинга: {text}"
        msg.attach(MIMEText(body, "plain"))
        text = msg.as_string()

        server = smtplib.SMTP_SSL(host="smtp.mail.ru", port=465)
        server.login(fromaddr, mypass)
        for reciever in recievers:
            server.sendmail(fromaddr, reciever, text)
        server.quit()
    except Exception as e:
        print(e)
        return HttpResponse(status=500)

    return HttpResponse(status=200)
