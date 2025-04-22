from django.urls import path

from django_solomon.views import validate_magic_link, magic_link_sent, send_magic_link

app_name = "django_solomon"

urlpatterns = [
    path(
        "magic-link/",
        send_magic_link,
        name="login",
    ),
    path(
        "magic-link/sent/",
        magic_link_sent,
        name="magic_link_sent",
    ),
    path(
        "magic-link/<str:token>/",
        validate_magic_link,
        name="validate_magic_link",
    ),
]
