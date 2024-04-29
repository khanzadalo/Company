import random
import string
from decouple import config
from django.core.mail import send_mail

from apps.users.models import User

code = random.randint(1000, 9999)
reset_password = random.randint(1000, 9999)


def send_email_confirmation(email):
    subject = "Подтверждение электронной почты"
    message = (
        f"Привет! Ваш адрес электронной почты был указан для входа на сайт Company. "
        f"Пожалуйста, введите этот код на странице входа в систему: {code}. "
        f"Если это были не вы или вы не регистрировались на сайте, просто проигнорируйте это письмо."
    )
    email_from = "nikksiri@yandex.ru"
    send_mail(subject, message, email_from, [email])
    user_obj = User.objects.get(email=email)
    user_obj.otp = code
    user_obj.save()


def send_email_reset_password(email, reset_password):
    subject = "Сброс пароля"
    message = (
        f"Код для сброса пароля: {reset_password}. Код действителен в течение 5 минут."
    )
    email_from = config('EMAIL_HOST_USER')
    send_mail(subject, message, email_from, [email])


def generate_random_code(length=4):
    characters = string.octdigits + string.digits
    return "".join(random.choice(characters) for _ in range(length))

