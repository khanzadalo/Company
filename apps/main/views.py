from rest_framework import permissions
from rest_framework.generics import UpdateAPIView, RetrieveAPIView, CreateAPIView, ListAPIView

from apps.main.models import Employee
from apps.main.serializers import EmployeeSerializers
from apps.common.common_exceptions import OnlyAdmin

from apps.main.serializers import EmployeeCreateSerializers


class IsOwnerOrAdminOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.groups.filter(name='admin').exists() or obj.user == request.user:
            return True
        return False


class IsAdminOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='admin').exists():
            return True
        return False


class EmployeeCreateApi(CreateAPIView):
    serializer_class = EmployeeCreateSerializers
    queryset = Employee.objects.all()

    permission_classes = ()


class EmployeeApi(RetrieveAPIView, UpdateAPIView):

    def perform_update(self, serializer):
        if serializer.validated_data.get('position'):
            if self.request.user.groups.filter(name='admin').exists() is False:
                raise OnlyAdmin()
        super().perform_update(serializer)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    serializer_class = EmployeeSerializers
    queryset = Employee.objects.all()

    permission_classes = (IsOwnerOrAdminOnly,)


class EmployeeListApi(ListAPIView):
    serializer_class = EmployeeSerializers

    def get_queryset(self):

        queryset = Employee.objects.all()
        username = self.request.query_params.get('username', None)
        departament = self.request.query_params.get('departament', None)
        position = self.request.query_params.get('position', None)
        if username is not None:
            queryset = queryset.filter(name__contains=username)
        if departament is not None:
            queryset = queryset.filter(position_departament__departament__title=departament)
        if position is not None:
            queryset = queryset.filter(position_departament__title=position)

        return queryset
