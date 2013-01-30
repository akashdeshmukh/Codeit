import os, sys

path = '/home/tripples/CJ/'

if path not in sys.path:
   sys.path.append(path)


os.environ['DJANGO_SETTINGS_MODULE'] = 'CJ.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
