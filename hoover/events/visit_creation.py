import os, sys
from datetime import datetime

path='/home/sheefrex/code/cattalax/site' # ntc
if path not in sys.path:
	sys.path.append(path)

os.environ["DJANGO_SETTINGS_MODULE"]="cattalax.settings"

from django.core.management import setup_environ
from cattalax import settings
from dashboard.models import Customer, Outlet, Visit

setup_environ(settings)

import MySQLdb
from duration import *
HOST="localhost"
USER="root"
PW="the power to do what is right"
DB="cattalax"

con = MySQLdb.connect(HOST,USER,PW,DB)
cur = con.cursor()

shop_list = [1, 13]

def captures_in_shop(shop_no, cursor):
	view = "capture"+str(shop_no) # Enter view name
	# Get the shop enter view in csv form
	cursor.execute("SELECT id FROM "+view+" WHERE obs>2 INTO OUTFILE '/tmp/list_of_enters.csv' fields terminated by ',' ENCLOSED BY '\"' LINES TERMINATED BY '\\n'")
	# Get the list of addresses
	file_of_addrs = open("/tmp/id_list.csv")
	addrs = file_of_addrs.read().split()
	os.remove('tmp/id_list.csv')
	return addrs

def walkbys_in_shop(shop_no, cursor):
	cursor.execute("SELECT id, timestamp FROM attendance WHERE rssi<-70 AND sensor_id="+shop_no+" GROUP BY id INTO OUTFILE '/tmp/walkbys.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\\n'")
	file_of_walkbys = open("/tmp/walkbys.csv")
	walkbys = file_of_walkbys.read().split()
	os.remove('tmp/walkbys.csv')
	return walkbys

def behaviour_summary(address, cursor):
	filename = '/tmp/detail.csv'
	sql_command = "SELECT DISTINCT * FROM attendance WHERE id="+addr+" ORDER BY timestamp, -rssi INTO OUTFILE '"+filename+"' FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\\n'"
	cursor.execute(sql_command)
	print "Getting duration, and inserting to customer_log table."
	g_d = robjects.r('get_duration(\"' + filename + '\")')
	return g_d

def customer_search(mac_addr):
	if len(Customer.objects.filter(mac_addr=eval(addr)))==0:
		c = Customer(mac_addr=eval(addr))
		c.save()
	else:
		c = Customer.objects.get(mac_addr=g_d[count])
	return c

def month_search(dt, outlet):
	try:
		m= Month.objects.get(vendor=outlet, month_no=dt.month, year=dt.year)
	except (ValueError, ObjectDoesNotExist):
		m = Month(year=dt.year, month_no=dt.month, vendor=outlet, no_of_walkbys=0, no_of_bounces=0, no_of_entries=0, avg_duration=0)
		m.save()
	return m

def week_search(dt, outlet):
	try:
		w= Week.objects.get(vendor=outlet, week_no=dt.isocalender()[1], year=dt.year)
	except (ValueError, ObjectDoesNotExist):
		w = Week(year=dt.year, week_no=dt.isocalender()[1], vendor=outlet, no_of_walkbys=0, no_of_bounces=0, no_of_entries=0, avg_duration=0)
		w.save()
	return w

def day_search(dt, outlet, week, month):
	try:
		d = Day.objects.get(vendor=outlet, over_week=week, over_month=month)
	except (ValueError, ObjectDoesNotExist):
		d = Day(year=dt.year, month=dt.month, day=dt.day, datetime=dt, over_week=week, over_month=month, vendor=outlet, no_of_walkbys=0, no_of_bounces=0, no_of_entries=0, avg_duration=0)
		d.save()
	return d

for shop_no in shop_list:
	outlet = Outlet.objects.get(sensor_no=shop_no)
	captures = captures_in_shop(shop_no, cur)
	walkbys = walkbys_in_shop(shop_no, cur)
	for walkby in walkbys:
		entry = walkby.split(',')
		timestamp = int(eval(entry[1]))
		addr = entry[0]
		dt = datetime.fromtimestamp(timestamp)
		w = Walkby(vendor=shop, time=timestamp, datetime=dt)
		w.save()
		print "Walkby recorded"

	for addr in captures:
		customer = customer_search(addr)
		g_d = behaviour_summary(addr, cur)
		visits = len(g_d)/4
		count = 0
		for i in range(visits):
			v = Visit(patron=customer, vendor=outlet, arrival_time=int(g_d[count+1]), duration=int(g_d[count+2]))
			v.save()
			count += 4
