import os, sys

path='/root/.virtualenvs/cattalax/cattalax'
if path not in sys.path:
	sys.path.append(path)

os.environ["DJANGO_SETTINGS_MODULE"]="cattalax.settings"

from django.core.management import setup_environ
from cattalax import settings
from dashboard.models import Customer, Outlet, Visit, Walkby, Day, Hour

setup_environ(settings)

list_of_shops = [v for v in Outlet.objects.all()]

for shop in list_of_shops:
	days_to_update = shop.day_set.filter(datetime__gte=timezone.now()-datetime.timedelta(days=7))	
	for day in days_to_update:
		list_of_visits = [visit for visit in day.visit_set.all()]
		day.no_of_entries = len(list_of_visits)

		list_of_walkbys = [walkby for walkby in day.walkby_set.all()]
		day.no_of_walkbys = len(list_of_walkbys)

		list_of_bounces = [v for v in list_of_visits if v.duration<60]
		day.no_of_bounces = len(list_of_bounces)

		if d.no_of_entries>0:
			day.avg_duration = sum([int(v.duration) for v in list_of_visits])/hour.no_of_entries

		d.save()

		for hour in day.hour_set.all():
			list_of_visits = [visit for visit in hour.visit_set.all()]
			hour.no_of_entries = len(list_of_visits)

			list_of_walkbys = [walkby for walkby in hour.walkby_set.all()]
			hour.no_of_walkbys = len(list_of_walkbys)

			list_of_bounces = [v for v in list_of_visits if v.duration<60]
			hour.no_of_bounces = len(list_of_bounces)

			if hour.no_of_entries>0:
				hour.avg_duration = sum([int(v.duration) for v in list_of_visits])/hour.no_of_entries

			hour.save()


