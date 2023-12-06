from . import views
from .views import ServiceList, ServiceDetail
from django.urls import path


urlpatterns = [
    path('', ServiceList.as_view(), name='home'),
    path('<slug:slug>/', ServiceDetail.as_view(), name='service_detail'),
]
