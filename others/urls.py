from django.urls import path

from . import views

urlpatterns = [
    path('others/send-message/', views.MessageView.as_view(), name="send-message")
]