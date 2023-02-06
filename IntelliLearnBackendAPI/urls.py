from django.urls import path, include
from IntelliLearnBackendAPI import views

urlpatterns = [

    path('addMcq', views.McqsAPIView.as_view(), name='addMcq'),
    path('addStudent', views.StudentsAPIView.as_view(), name='addStudent'),
    path('addClass', views.ClassesAPIView.as_view(), name='addClass'),
    path('', views.home, name='home')

]