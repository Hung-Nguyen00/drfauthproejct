from django.urls import path
from student.api.views import StudentList, StudentDetail

urlpatterns = [
    path('', StudentList.as_view()),
    path('<int:pk>', StudentDetail.as_view()),
]