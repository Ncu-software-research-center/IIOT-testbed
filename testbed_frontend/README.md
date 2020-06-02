# Testbed Frontend

## Introduction

**Testbed frontend** that let the user to interact
with the system’s user interface through a website.

## Prerequisites

### os

| OS     | VERSION | BIT   |
|--------|---------|-------|
| Ubuntu | 18.04   | 32/64 |

### Package

| Package        | VERSION |
|----------------|---------|
| Docker         | 19.03.2 |
| Docker-compose | 3.0     |

## Download

The source code may be downloaded from the Git repository using the following command on the command line.

```
git clone https://github.com/Airwavess/testbed/
```

## Configure

Config files are stored in the `api/emulation/__init__.py` and `website/src/config.js`. You should set these environment variable before install Testbed.

### `api/emulation/__init__.py`

```
class Config:
    FRONTEND_IP = '{FRONTEND_IP}'
    REDIS_PORT = 6379
    REDIS_PASSWORD = 'redispass'
```

### `website/src/config.js`

```
export const ApiHost = 'http://{FRONTEND_IP}:8000/api'
```

### `testbed/settings.py`

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djangomysql',
        'USER': 'test',
        'PASSWORD': 'test1234',
        'HOST': '{FRONTEND_IP}',
        'PORT': '3306'
    }
}
```

## Install

### Build and deploy Testbed

Once the report directory is generated then use the following commands from the testbed directory to install.

```
docker-compose build
docker-compose up -d
```

### Create a new user

After the Testbed deployment is completed, the user must have their own account and password to log in to Testbed and enter the Dashboard. Therefore, the user must use the following command to create their own account and password.

```
./wait-for-it.sh 0.0.0.0:3306 --timeout=60 && docker-compose run web python manage.py createsuperuser
```
