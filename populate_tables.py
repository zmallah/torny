#!/usr/bin/env python
import pymysql
pymysql.install_as_MySQLdb()

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'torny_backend.settings')

import django
django.setup()



from torny_backend.models import Role, Event

role1 = Role(id=1, role='Fencer')
role2 = Role(id=2, role='Orignizer')
role3 = Role(id=3, role='Director')

role1.save()
role2.save()
role3.save()

event1 = Events(id=1, event_type='touch_scored')
event2 = Events(id=2, event_type='yellow_card')
event3 = Events(id=3, event_type='red_card')
event4 = Events(id=4, event_type='black_card')
event5 = Events(id=5, event_type='bout_over')

event1.save()
event1.save()
event2.save()
event3.save()
event4.save()
event5.save()
