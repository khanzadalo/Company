from django.db import models
from apps.common.models import BaseModel
from apps.users.models import User


class Department(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Name")

    def __str__(self):
        return self.name


class Position(models.Model):
    POSITION_CHOICES = (
        ('manager', 'Manager'),
        ('developer', 'Developer'),
        ('designer', 'Designer'),
        ('qa_engineer', 'QA Engineer'),
        ('sales', 'Sales'),
        ('marketing', 'Marketing'),
        ('hr', 'HR'),
        ('other', 'Other')
    )

    title = models.CharField(max_length=255, choices=POSITION_CHOICES)

    def __str__(self):
        return self.title


class Employee(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee")
    username = models.CharField(max_length=255, verbose_name="Username")
    surname = models.CharField(max_length=255, verbose_name="Surname")
    first_name = models.CharField(max_length=255, verbose_name="First Name")
    last_name = models.CharField(max_length=255, verbose_name="Last Name")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Department")
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True, verbose_name="Avatar")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name="Position")
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Salary")
    is_admin = models.BooleanField(default=False, verbose_name="Is Admin")
    email = models.EmailField(max_length=255, verbose_name="Email")
    date_of_birth = models.DateField(verbose_name="Date of Birth")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PersonalData(BaseModel):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, verbose_name="Employee")
    address = models.CharField(max_length=255, verbose_name="Address")
    bank_book = models.CharField(max_length=255, verbose_name="Bank Book")

    def __str__(self):
        return self.employee.username
