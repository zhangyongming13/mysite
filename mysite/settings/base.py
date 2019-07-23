import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'ckeditor',
    'ckeditor_uploader',
    'read_statistics',
    'comment',
    'likes',
    'user',
    'notifications',
    'my_notifications',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 设置全局模板文件夹，BASE_DIR是整个django全局文件夹
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'user.context_processors.login_modal_form',  # 将LoginForm作为想user一样的类似全局变量的方式
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static_collected')  # 设置将其他目录的css文件收集到一个目录中
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static'),
]

# media文件夹用来存放上传的图片
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 配置ckeditor
CKEDITOR_UPLOAD_PATH = 'upload'

EACH_PAGE_BLOG_NUMBER = 10

# 设置数据库缓存
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}

# ckeditor设置，设置名为my_config
CKEDITOR_CONFIGS = {
    'default':{},
    'comment_ckeditor':{
        'toolbar': 'custom',
        'toolbar_custom': [  # 工具栏项目
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript'],
            ["TextColor", "BGColor", 'RemoveFormat'],
            ['NumberedList', 'BulletedList'],
            ['Link', 'Unlink'],
            ["Smiley", "SpecialChar", 'Blockquote'],
        ],
        'width': 'auto',
        'height': '180',
        'tabSpaces': 4,
        'removePlugins': 'elementspath',  # 去掉底框
        'resize_enabled': False,
    },
    'my_config': {
        'skin': 'moono-lisa',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar': (['div', 'Source', '-', 'Save', 'NewPage', 'Preview', '-', 'Templates'],
                    ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Print', 'SpellChecker', 'Scayt'],
                    ['Undo', 'Redo', '-', 'Find', 'Replace', '-', 'SelectAll', 'RemoveFormat', '-', 'Maximize',
                     'ShowBlocks', '-', "CodeSnippet", 'Subscript', 'Superscript'],
                    ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                     'HiddenField'],
                    ['Bold', 'Italic', 'Underline', 'Strike', '-'],
                    ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', 'Blockquote'],
                    ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
                    ['Link', 'Unlink', 'Anchor'],
                    ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak'],
                    ['Styles', 'Format', 'Font', 'FontSize'],
                    ['TextColor', 'BGColor'],
                    ),
        'extraPlugins': ','.join(['codesnippet', 'prism', 'widget', 'lineutils']),
        # 'extraPlugins': 'codesnippet',
    },
    # 创建博客的ckeditor的样式
    'create_blog': {
            'skin': 'moono-lisa',
            'toolbar_Basic': [
                ['Source', '-', 'Bold', 'Italic']
            ],
            'toolbar': (['div', 'Source', '-', 'Save', 'NewPage', 'Preview', '-', 'Templates'],
                        ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Print', 'SpellChecker', 'Scayt'],
                        ['Undo', 'Redo', '-', 'Find', 'Replace', '-', 'SelectAll', 'RemoveFormat', '-', 'Maximize',
                         'ShowBlocks', '-', "CodeSnippet", 'Subscript', 'Superscript'],
                        ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                         'HiddenField'],
                        ['Bold', 'Italic', 'Underline', 'Strike', '-'],
                        ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', 'Blockquote'],
                        ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
                        ['Link', 'Unlink', 'Anchor'],
                        ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak'],
                        ['Styles', 'Format', 'Font', 'FontSize'],
                        ['TextColor', 'BGColor'],
                        ),
            # 'extraPlugins': 'codesnippet',
            'extraPlugins': ','.join(['codesnippet', 'prism', 'widget', 'lineutils']),
            'width': '100%',
            'height': '600',
            'tabSpaces': 4,
            'removePlugins': 'elementspath',  # 去掉底框
            'resize_enabled': False,
        }
}

# 使得notifications发送通知的时候可以额外携带一些数据，比如url
DJANGO_NOTIFICATIONS_CONFIG = { 'USE_JSONFIELD': True}
