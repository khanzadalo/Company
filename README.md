# Company
## EMS - Employee Management 

## Настройка
Для начала работы с проектом вам потребуется клонировать репозиторий на свой компьютер. Вы можете сделать это, используя следующие команды:
```bash
git clone https://github.com/khanzadalo/Company.git
cd Company
python -m venv venv
source venv/bin/activate Linux
venv\Scripts\activate   Windows
pip install -r requirements.txt
```
Для настройки проекта вам потребуется файл .env, в котором будут храниться ваши переменные окружения. Пример содержимого файла .env:
```bash
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost
PRODUCTION=False

POSTGRES_DB=your-database-name
POSTGRES_USER=your-database-user
POSTGRES_PASSWORD=your-database-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

EMAIL_USE_SSL=True
EMAIL_PORT=465
EMAIL_HOST=your-email-host
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-email-password
```

## Запуск проекта
После создания файла .env, вы можете запустить проект, используя следующие команды:
```bash
python manage.py runserver
```

## Контакты
Если вы нашли ошибки или у вас есть вопросы или предложения, свяжитесь со мной по адресу https://t.me/nikksiri