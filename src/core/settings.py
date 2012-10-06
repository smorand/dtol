# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

import sys
import os
import codecs
import re
import springpython.config

# APPLICATION_ROOT and CONFIG
APPLICATION_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.environ['DJANGO_PROJECT_CONFIG'] if 'DJANGO' in os.environ else APPLICATION_ROOT + os.path.sep + 'resources' + os.path.sep + 'config.properties'

config = {}

reg_comment = re.compile('#.*')
with codecs.open(CONFIG_FILE, 'r', 'utf8') as f:
	for row in f:
		rowclean = reg_comment.sub('', row).strip()
		if len(rowclean) > 0:
			vals = rowclean.split('=')
		if len(vals) == 2:
			key, value = vals[0], vals[1] 
			config[key.strip()] = value.strip().replace('%APPLICATION_ROOT%', APPLICATION_ROOT)
		else:
			sys.stderr.write('Line %s is not conform in configuration file')

EXTERNAL_PATH = config['external_path'].split(':') if 'external_path' in config else []

DEBUG_GENERIC = 'APACHE_RUN_DIR' not in os.environ
DEBUG = config['debug'] in ['true', '1'] if 'debug' in config else DEBUG_GENERIC 
TEMPLATE_DEBUG = DEBUG

ADMINS = False
if 'admins' in config:
	for admin in config['admins'].split(';'):
		adminname, adminemail = admin.split('/')
		if ADMINS == False:
			ADMINS = ((adminname.strip(), adminemail.strip()), )
		else:
			ADMINS += ((adminname.strip(), adminemail.strip()),)
else:
	ADMINS = (
		('No admin', 'noadmin@nomail.com'),
	)

MANAGERS = False
if 'admins' in config:
	for admin in config['admins'].split(';'):
		adminname, adminemail = admin.split('/')
		if MANAGERS == False:
			MANAGERS = ((adminname.strip(), adminemail.strip()), )
		else:
			MANAGERS += ((adminname.strip(), adminemail.strip()),)
else:
	MANAGERS = ADMINS

DATABASES = {}
if 'databases' in config:
	for database in config['databases'].split(','):
		DATABASES[database] = {
			'ENGINE': config['database_%s_engine' % database] if 'database_%s_engine' % database in config else '',					# Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
			'NAME': config['database_%s_name' % database] if 'database_%s_name' % database in config else '',						# Or path to database file if using sqlite3.
			'USER': config['database_%s_user' % database] if 'database_%s_user' % database in config else '',								# Not used with sqlite3.
			'PASSWORD': config['database_%s_password' % database] if 'database_%s_password' % database in config else '',	# Not used with sqlite3.
			'HOST': config['database_%s_host' % database] if 'database_%s_host' % database in config else '',								# Set to empty string for localhost. Not used with sqlite3.
			'PORT': config['database_%s_port' % database] if 'database_%s_port' % database in config else '',								# Set to empty string for default. Not used with sqlite3.
		}
if len(DATABASES) == 0:
	DATABASES['default'] = {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': 'project.db'
	}

# URL ROOT
URL_ROOT = config['url_root'] if 'url_root' in config else 'http://localhost:8000'

# SMTP Authentication
SMTP_AUTH = {
	'server': config['smtp_auth_server'] if 'smtp_auth_server' in config else '',
	'port': int(config['smtp_auth_port']) if 'smtp_auth_port' in config else 25,
	'username': config['smtp_auth_username'] if 'smtp_auth_username' in config else '',
	'password': config['smtp_auth_password'] if 'smtp_auth_password' in config else '',
	'subjectheader': config['smtp_auth_server'] if 'smtp_auth_subjectheader' in config else '',
	'from': config['smtp_auth_from'] if 'smtp_auth_from' in config else '',
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = config['timezone'] if 'timezone' in config else ''

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = config['language'] if 'language' in config else 'en'
_ = lambda s: s
LANGUAGES=False
if 'languages' in config:
	for lang in config['languages'].split(';'):
		langcode, langlib = lang.split('/')
		if LANGUAGES == False:
			LANGUAGES = ((langcode.strip(), _(langlib.strip())), )
		else:
			LANGUAGES += ((langcode.strip(), _(langlib.strip())),)
else:
	LANGUAGES = (
	  ('en', _('English')),
	)

LOCALE_PATHS = ( APPLICATION_ROOT + os.path.sep + 'locale', )
LANGUAGE_COOKIE_NAME='lang'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: '/home/media/media.lawrence.com/'
STATIC_ROOT = APPLICATION_ROOT + os.path.sep + 'static' + os.path.sep

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: 'http://media.lawrence.com', 'http://example.com/media/'
#MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
#ADMIN_MEDIA_PREFIX = '/adminstatic/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'r8v)-*8v$9zp%(kky^myj+x7k6336mn1_stn7_6f(^n=v0hm=7'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
	#'django.template.loaders.eggs.Loader',
)

TEMPLATE_STRING_IF_INVALID = '***'

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.locale.LocaleMiddleware',
	'django.middleware.common.CommonMiddleware',
	#'django.middleware.csrf.CsrfViewMiddleware',
	#'django.contrib.auth.middleware.AuthenticationMiddleware',
	#'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
	# Put strings here, like '/home/html/django_templates' or 'C:/www/django/templates'.
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
	APPLICATION_ROOT + os.path.sep + 'templates'
)

INSTALLED_APPS = (
	#'django.contrib.auth',
	#'django.contrib.contenttypes',
	'django.contrib.sessions',
	'core',
	#'django.contrib.sites',
	#'django.contrib.messages',
	# Uncomment the next line to enable the admin:
	#'django.contrib.admin',
)
for app in config['installedapps'].split(','):
	INSTALLED_APPS += (app, )

APPLICATION_CONTEXT_PATH = APPLICATION_ROOT + os.path.sep + 'resources' if 'context_path' not in config else config['context_path'] 
APPLICATION_CONTEXTS = [ springpython.config.XMLConfig(APPLICATION_CONTEXT_PATH + os.path.sep + 'applicationContext.xml') ] if 'contexts' not in config else [ springpython.config.XMLConfig(APPLICATION_CONTEXT_PATH + os.path.sep + f.strip() + '.xml') for f in config['contexts'].split(',') ]

LOGGING = {
	'version': 1,
	'disable_existing_loggers': True,
	'formatters': {
		'verbose': {
				'format': '[%(asctime)s] %(levelname)s %(module)s %(process)d %(thread)d: %(message)s'
		},
	},
	'handlers': {
		'console': {
			'level':'DEBUG',
			'class':'logging.StreamHandler',
			'formatter': 'verbose'
		},
		'generic': {
			'level':'INFO',
			'class': 'logging.handlers.TimedRotatingFileHandler',
			'formatter': 'verbose',
			'filename': 'project.log',
			'when': 'D',
			'backupCount': '0',
		},
		'mail_admins': {
			'level': 'ERROR',
			'class': 'django.utils.log.AdminEmailHandler',
			'formatter': 'verbose',
		},
	},
	'loggers': {
		'django': {
			'handlers': ['generic', 'console'],
			'propagate': True,
			'level':'WARNING',
		},
		'django.request': {
			'handlers': ['generic', 'console'],
			'level': 'WARNING',
			'propagate': False,
		},
		'app': {
			'handlers': ['generic', 'console'],
			'level': 'DEBUG' if DEBUG else 'INFO',
			'propagate': False,
		},
	}
}
