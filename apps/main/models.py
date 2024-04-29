from django.db import models

from apps.common.models import BaseModel
from apps.users.models import User


class Departament(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Name")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департаменты'


class PositionDepartament(models.Model):
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
    departament = models.ForeignKey(Departament, on_delete=models.CASCADE)

    def __str__(self):
        return "депортамент %s позиция %s" % (self.departament, self.title)

    class Meta:
        verbose_name = 'Позиция в департаменте'
        verbose_name_plural = 'Позиции в департаменте'


class Employee(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Сотрудник")
    username = models.CharField(max_length=255, verbose_name="Имя пользователя")
    surname = models.CharField(max_length=255, verbose_name="Фамилия")
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255, verbose_name="Отчество")
    department = models.ForeignKey(Departament, on_delete=models.CASCADE, verbose_name="Департаменте")
    avatar = models.ImageField(upload_to="avatars/", default='avatars/friend.jpg', verbose_name="Аватар")
    position = models.ForeignKey(PositionDepartament, null=True, on_delete=models.SET_NULL, verbose_name="Позиция")
    salary = models.FloatField(default=0, verbose_name="Зарплата")
    is_admin = models.BooleanField(default=False, verbose_name="Админ")
    email = models.EmailField(max_length=255, verbose_name="Email")
    date_of_birth = models.DateField(verbose_name="Дата рождения")

    def __str__(self):
        return "%s, %s" % (self.username, self.position)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class PersonalData(BaseModel):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, verbose_name="Сотрудник")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    bank_book = models.CharField(max_length=255, verbose_name="Банковская книжка")



