from . import views
from django.urls import path


urlpatterns = [
    path('', views.ServiceList.as_view(), name='home'),
    path('<slug:slug>/', views.ServiceDetail.as_view(), name='service_detail'),
]
