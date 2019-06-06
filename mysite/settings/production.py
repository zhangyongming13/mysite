import os
from .base import *


SECRET_KEY = os.environ['SECRET_KEY']


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['192.168.1.247', '192.168.1.112', '10.19.110.13', 'http://mingtiantianshi.pythonanywhere.com/', '192.168.1.111', '192.168.42.193', '47.112.108.255']


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES_PASSWORD = os.environ['DATABASES_PASSWORD']
# 使用mysql的数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysite_db',
        'USER': 'zhang',
        'PASSWORD': DATABASES_PASSWORD,
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# 发送邮件设置
# https://docs.djangoproject.com/en/2.0/ref/settings/#email
# https://docs.djangoproject.com/en/2.0/topics/email/

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'mingtiantianshi16@163.com'
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']  # 授权码
EMAIL_SUBJECT_PREFIX = '[小明的博客] '
EMAIL_USE_SSL = True  # 与SMTP服务器通信时，是否启动SSL链接(安全链接)

# 管理人员以及邮箱账号
ADMINS = (
    ('admin', 'mingtiantianshi13@163.com'),
)

# 日志文件
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用django自身的日志记录器
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/home/mysite_debug.log',
        },
        'mail_admins': {  # 发生错误的时候发送邮件给管理人员
                    'level': 'ERROR',
                    'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
                    'handlers': ['mail_admins'],
                    'level': 'ERROR',
                    'propagate': False,
        },
    },
}
