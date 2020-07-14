DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'account',
        'USER': 'website',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    },
    'player': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'player',
        'USER': 'website',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

DATABASE_ROUTERS = ['website.settings.db_routers.Player', 'website.settings.db_routers.Account']
