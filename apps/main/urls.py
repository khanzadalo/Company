from django.urls import path
from .views import (EmployeeListView, EmployeeDetailView,
                    DepartmentDetailView, DepartmentListView)

urlpatterns = [
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('departments/', DepartmentListView.as_view(), name='department-list'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('departments/<int:pk>/', DepartmentDetailView.as_view(), name='department-detail'),

]