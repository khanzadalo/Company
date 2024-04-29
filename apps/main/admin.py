from django.contrib import admin
from .models import Employee, Departament, PositionDepartament

admin.site.register(Departament)
admin.site.register(PositionDepartament)
admin.site.register(Employee)
