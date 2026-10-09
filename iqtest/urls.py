from django.urls import path

from . import views

app_name = "iqtest"

# The fixed pass/ and result/ routes must come before <slug:slug>/, or
# "pass" and "result" would be treated as test slugs.
urlpatterns = [
    path("", views.test_list, name="test_list"),
    path("pass/success/", views.pass_success, name="pass_success"),
    path("pass/<str:token>/", views.pass_detail, name="pass_detail"),
    path("result/<int:pk>/", views.result_detail, name="result_detail"),
    path("<slug:slug>/buy/", views.buy_pass, name="buy_pass"),
    path("<slug:slug>/", views.take_test, name="take_test"),
]
