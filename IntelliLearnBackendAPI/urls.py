from django.urls import path, include
from IntelliLearnBackendAPI import views

urlpatterns = [

    path('addMcq', views.McqsAPIView.as_view(), name='addMcq'),
    path('', views.home, name='home')

]