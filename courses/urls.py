from django.urls import path

from . import views

app_name = "courses"

urlpatterns = [
    path("", views.course_list, name="course_list"),
    path("<slug:slug>/", views.course_detail, name="course_detail"),
    path("<slug:course_slug>/enroll/", views.enroll, name="enroll"),
    path("<slug:course_slug>/lesson/<int:lesson_id>/", views.lesson_detail, name="lesson_detail"),
    path("<slug:course_slug>/lesson/<int:lesson_id>/complete/", views.mark_complete, name="mark_complete"),
]
