from django.urls import path, include
from IntelliLearnBackendAPI import views

urlpatterns = [

    path('addMcq', views.McqsAPIView.as_view(), name='addMcq'),
    path('addStudent', views.StudentsAPIView.as_view(), name='addStudent'),
    path('addTeacher', views.TeacherAPIView.as_view(), name='addTeacher'),
    path('teacherClasses', views.TeacherClassesAPIView.as_view(), name='teacherClasses'),
    path('marksByEvaluationType', views.MarksByEvaluationType.as_view(), name='marksByEvaluationType'),
    path('teacherAttendance', views.TeacherAttendanceView.as_view(), name='teacherAttendance'),
    path('teacherAnnouncement', views.TeacherAnnouncementsAPIView.as_view(), name='teacherAnnouncement'),
    path('questionAnswering', views.QuestionAnswering.as_view(), name='questionAnswering'),
    path('addTeacherSchedule', views.TeacherScheduleView.as_view(), name='addTeacherSchedule'),
    path('askChatGPT', views.AskChatGPT.as_view(), name='askChatGPT'),
    path('loginTeacher', views.TeacherLoginAPIView.as_view(), name='loginTeacher'),
    path('addClass', views.ClassesAPIView.as_view(), name='addClass'),
    path('', views.home, name='home')

]