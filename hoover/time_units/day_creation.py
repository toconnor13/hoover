import os, sys

script, day, month, year = sys.argv

path='/home/sheefrex/code/cattalax/site'
if path not in sys.path:
	sys.path.append(path)

os.environ["DJANGO_SETTINGS_MODULE"]="cattalax.settings"

from django.core.management import setup_environ
from cattalax import settings
from dashboard.models import Customer, Outlet, Visit, Walkby, Day, Hour

setup_environ(settings)

list_of_shops = [v for v in Outlet.objects.all()]

for shop in list_of_shops:
	d = Day(vendor=shop, day=day, month=month, year=year, no_of_walkbys=0, no_of_entries=0, no_of_bounces=0, avg_duration=0)
	
	
	list_of_visits = [visit for visit in shop.visit_set.all()]
	d.no_of_entries = len(list_of_visits)

	list_of_walkbys = [walkby for walkby in shop.walkby_set.all()]
	d.no_of_walkbys = len(list_of_walkbys)

	list_of_bounces = [v for v in list_of_visits if v.duration<60]
	d.no_of_bounces = len(list_of_bounces)

	if d.no_of_entries>0:
		d.avg_duration = sum([int(v.duration) for v in list_of_visits])/d.no_of_entries

	print "Day object created"

	d.save()


	for j in range(24):
		h = Hour(vendor=shop, day=d, hour=j, no_of_walkbys=0, no_of_entries=0, no_of_bounces=0, avg_duration=0)
		visits_this_hour = [v for v in list_of_visits if v.get_hour()==j]
		h.no_of_entries = len(visits_this_hour)
#		print len(visits_this_hour)
#		print h.no_of_entries

		if h.no_of_entries>0:
			h.avg_duration = sum([int(v.duration) for v in visits_this_hour])/h.no_of_entries
		
		h.no_of_walkbys = len([w for w in list_of_walkbys if w.get_hour()==j])
		h.no_of_bounces = len([b for b in list_of_bounces if b.get_hour==j])
		print "Hour object created for " + str(h)
		h.save()








