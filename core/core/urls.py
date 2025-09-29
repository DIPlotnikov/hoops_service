"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import jwt
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from otp.views import verify_otp
from .mid_logger import LogAllRequests


class AuthMiddleWare(object):
    def resolve(self, next, root, info, **args):

        try:

            token = info.context.headers.get("Authorization").split(" ")[1]
            if token is None:
                token = info.context.headers.get(b"authorization").decode("utf-8").split(" ")[1]
            try:
                retoken = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                print(retoken)
            except:
                print("err")
                raise jwt.ExpiredSignatureError

            info.context.user.pk = retoken.get("id")
            info.context.user.id = retoken.get("role")
            # info.context.user.is_authenticated = True
            read = retoken.get("read")
            if read:
                if info.parent_type.name == "Mutation":
                    raise ValueError("Не достаточно прав")

        except ValueError:
            raise ValueError("Недостаточно прав")
        except jwt.ExpiredSignatureError:
            raise ValueError("Сессия завершена")
        except:
            pass

        return next(root, info, **args)


urlpatterns = [
    path("admin/login/", verify_otp, name="verify_otp"),
    path("admin/", admin.site.urls),
    path(
        "graphql/",
        csrf_exempt(
            GraphQLView.as_view(
                graphiql=True,
                middleware=[
                    AuthMiddleWare(),
                    LogAllRequests(),
                ],
            )
        ),
    ),
]
urlpatterns += staticfiles_urlpatterns()
