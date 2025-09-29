from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from otp.models import OTP


def verify_otp(request):
    if request.method == "POST":
        username = request.POST.get("username")
        otp_code = request.POST.get("otp_code")
        print(username, otp_code)

        if not username:
            return render(request, "otp_login.html", {"error_message": "Пожалуйста, заполните имя пользователя."})

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist as e:
            print(e)
            return render(request, "otp_login.html", {"error_message": "Неверное имя пользователя."})

        if not otp_code:
            print("not OTP")
            OTP.objects.filter(user=user).delete()
            otp = OTP()
            otp.user = user
            otp.save()
            return render(request, "otp_login.html", context={"flag": True, "username": username})

        try:
            otp = OTP.objects.filter(user=user).last()
            print(otp)
            assert otp is not None, "otp is none"
        except Exception as e:
            print(e)
            return render(request, "otp_login.html", {"error_message": "Неправильный код OTP.", "username": username})

        # Проверяем, не истек ли срок действия кода
        if not otp.verify(code=otp_code):
            return render(request, "otp_login.html", {"error_message": "Код неверный.", "username": username})

        # Логин пользователя
        user.backend = "django.contrib.auth.backends.ModelBackend"  # Устанавливаем backend для аутентификации
        login(request, user)
        return redirect("/admin/")  # Перенаправляем в административную панель

    return render(request, "otp_login.html")
