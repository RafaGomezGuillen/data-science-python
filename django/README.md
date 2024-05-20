# Django

## Install and set up Django and Django Rest Framework

### Install Django, djangorestframework and pip install django-cors-headers

```cmd
pip install Django
pip install djangorestframework
pip install django-cors-headers
```

### Create Django Project

```cmd
django-admin startproject <name_project> .
```

### Setting-up Django Rest Framework

At `<name_project>/settings.py`

```py
ALLOWED_HOSTS = ['*']

CORS_ALLOWED_ORIGINS = [
    'http://localhost',
    'http://127.0.0.1',
    'http://0.0.0.0',
    # 'http://localhost:5173' Frontend URL
]

CORS_ALLOW_CREDENTIALS = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', # New installed app
    'corsheaders', # New installed app
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # New middleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

## Run the project

```cmd
python manage.py runserver
```

## Create Django App

```cmd
python manage.py startapp <name_app>
```

Add the created name app into "INSTALLED_APPS" list

```py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    '<name_app>',
    '<name_app>'
]
```

## Data migration to DB

Migrate the existing tables to database.

```cmd
python manage.py migrate <app>
```

Migrate a created or modified model to app/migrations/file.py.

```cmd
python manage.py makemigrations <name_app>
```

## Create an user admin (createsuperuser)

```cmd
python manage.py createsuperuser
```

## Add Swagger Documentation

[Swagger Doc Page Installation](https://drf-yasg.readthedocs.io/en/stable/readme.html)

## Create values in Database (Shell)

- Run `python manage.py shell` to go to the python shell.
- `from myapp.models import Project, Task` to import all models.
- `p = Object(field="Field 1")` to create an instance.
- `p.save()` to save it on DB.
- `Object.objects.all()` to see all saved values.
- `Object.objects.get(filed="Filed")` to see a particular saved value/s.
- `p = Object.objects.get(id=1)` to save an instance in a variable.
- `myp.task_set.create(field="task", field="desc")` to crate a task to a particular project.
- `exit()` to exit the python command shell.

## React set up

### Install vite

1. Run `npm create vite` to create a vite enviromet. This needs to be done in root folder and in other terminal.
   - Select React JS as Framework and follow the cmd indications.
2. Now install the following dependencies in client folder:
   - `npm i react-router-dom`
   - `npm i react-hot-toast`
   - `npm i axios`
   - `npm i react-hook-form`

### Install Tailwind CSS

- Check [Install Tailwind CSS with Vite](https://tailwindcss.com/docs/guides/vite)

## Video

- [Django REST Framework y React CRUD](https://www.youtube.com/watch?v=38XWpyEK8IY&list=PLr_kZfQvM56mjjCTYY5R2rTC8FmeP_3Tn&index=8&t=868s&ab_channel=FaztCode)