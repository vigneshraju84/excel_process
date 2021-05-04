from django.urls import path
from . import views

urlpatterns = [
	path('', views.xl_process, name="xl_process"),
]