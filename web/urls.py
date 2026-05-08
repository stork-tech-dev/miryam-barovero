from django.urls import path

from .views import ContactameView, EneagramaView, HomeView, RetirosView, SobreMiView

app_name = "web"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("eneagrama/", EneagramaView.as_view(), name="eneagrama"),
    path("retiros/", RetirosView.as_view(), name="retiros"),
    path("sobre-mi/", SobreMiView.as_view(), name="sobre_mi"),
    path("contactame/", ContactameView.as_view(), name="contactame"),
]
