# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import sys
import os
import django

#路径可能不对
sys.path.append('../../../mov_manage')
os.environ['DJANGO_SETTINGS_MODULE'] = 'mov_manage.settings'
django.setup()