from django.urls import path

from . import views

urlpatterns = [
    path('contact/', views.ContactPageView.as_view(), name="contact")
]