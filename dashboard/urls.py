from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.dashboard_index, name="dashboard_index"),
    path("chat-history/", views.chat_history, name="chat_history"),
    path("chat-history/<str:username>/", views.chat_history, name="chat_history_user"),
]
