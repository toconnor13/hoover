import os, sys

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

def ids_in_view(view, cursor):
	# Get the shop enter view in csv form
	cursor.execute("SELECT id FROM "+view+" WHERE obs>2 INTO OUTFILE '/tmp/list_of_enters.csv' fields terminated by ',' ENCLOSED BY '\"' LINES TERMINATED BY '\\n'")
	# Get the list of addresses
	file_of_addrs = open("/tmp/list_of_enters.csv")
	addrs = file_of_addrs.read().split()
	os.remove('tmp/cattalax/list_of_enters.csv')
	return addrs

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

for shop in shop_list:
	enter_view = "enter"+str(shop_list) # Enter view name
	addrs = ids_in_view(enter_view, cur)
	for addr in addrs:
		customer = customer_search(addr)
		g_d = behaviour_summary(addr, cur)
		visits = len(g_d)/4
		count = 0
		for i in range(visits):
			outlet = Outlet.objects.get(sensor_no=shop)
			v = Visit(patron=customer, vendor=outlet, arrival_time=int(g_d[count+1]), duration=int(g_d[count+2]))
			v.save()
			count += 4

