from django.urls import path

from . import views

app_name = "iqtest"

urlpatterns = [
    path("", views.test_list, name="test_list"),
    path("<slug:slug>/", views.take_test, name="take_test"),
    path("result/<int:pk>/", views.result_detail, name="result_detail"),
]
