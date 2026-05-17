from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .forms import StyledAuthenticationForm
from .news_views import (
    NewsAdminCreateView,
    NewsAdminDeleteView,
    NewsAdminListView,
    NewsAdminUpdateView,
    NewsDetailView,
    NewsListView,
    PanelView,
)
from .retreat_views import (
    RetreatAdminCreateView,
    RetreatAdminDeleteView,
    RetreatAdminListView,
    RetreatAdminUpdateView,
    RetreatDetailView,
)
from .views import (
    ContactameView,
    EneagramaView,
    EnneagramTestView,
    HomeView,
    RetirosView,
    SobreMiView,
)

app_name = "web"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("eneagrama/", EneagramaView.as_view(), name="eneagrama"),
    path("eneagrama/test/", EnneagramTestView.as_view(), name="enneagram_test"),
    path("retiros/", RetirosView.as_view(), name="retiros"),
    path("retiros/<slug:slug>/", RetreatDetailView.as_view(), name="retreat_detail"),
    path("sobre-mi/", SobreMiView.as_view(), name="sobre_mi"),
    path("contactame/", ContactameView.as_view(), name="contactame"),
    path("novedades/", NewsListView.as_view(), name="news_list"),
    path("novedades/<slug:slug>/", NewsDetailView.as_view(), name="news_detail"),
    path(
        "login/",
        LoginView.as_view(
            form_class=StyledAuthenticationForm,
            template_name="registration/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("panel/", PanelView.as_view(), name="panel"),
    path("panel/novedades/", NewsAdminListView.as_view(), name="news_admin_list"),
    path("panel/novedades/nueva/", NewsAdminCreateView.as_view(), name="news_admin_create"),
    path(
        "panel/novedades/<int:pk>/editar/",
        NewsAdminUpdateView.as_view(),
        name="news_admin_update",
    ),
    path(
        "panel/novedades/<int:pk>/eliminar/",
        NewsAdminDeleteView.as_view(),
        name="news_admin_delete",
    ),
    path("panel/retiros/", RetreatAdminListView.as_view(), name="retreat_admin_list"),
    path("panel/retiros/nuevo/", RetreatAdminCreateView.as_view(), name="retreat_admin_create"),
    path(
        "panel/retiros/<int:pk>/editar/",
        RetreatAdminUpdateView.as_view(),
        name="retreat_admin_update",
    ),
    path(
        "panel/retiros/<int:pk>/eliminar/",
        RetreatAdminDeleteView.as_view(),
        name="retreat_admin_delete",
    ),
]
