from django.urls import path

from apps.main.views import EmployeeApi, EmployeeCreateApi, EmployeeListApi

urlpatterns = [
    path('', EmployeeListApi.as_view(), name='employee_list'),
    path('<int:pk>/', EmployeeApi.as_view(), name='employee_detail'),
    path('create/', EmployeeCreateApi.as_view(), name='employee_create'),

]
