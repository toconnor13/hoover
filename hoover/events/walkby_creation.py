import os, sys

path='/home/sheefrex/code/cattalax/site'
if path not in sys.path:
	sys.path.append(path)

os.environ["DJANGO_SETTINGS_MODULE"]="cattalax.settings"

from django.core.management import setup_environ
from cattalax import settings
from dashboard.models import Customer, Outlet, Visit, Walkby

setup_environ(settings)

import MySQLdb
HOST="localhost"
USER="root"
PW="the power to do what is right"
DB="cattalax"

## TO DO:  need to make a loop out of this for each sensor id - so a double loop

con = MySQLdb.connect(HOST,USER,PW,DB)
cur = con.cursor()

cur.execute("SELECT timestamp, rssi FROM attendance WHERE rssi<-1 GROUP BY id INTO OUTFILE '/tmp/walkbys.csv' fields terminated by ',' ENCLOSED BY '\"' LINES TERMINATED BY '\\n'")



file_of_walkbys = open("/tmp/walkbys.csv")
walkbys = file_of_walkbys.read().split()

count = 0
for walkby in walkbys:
	entry = walkby.split(',')
	shop_no= 1
#	shop_no = int(entry[1])
	shop = Outlet.objects.get(sensor_no=shop_no)
	timestamp = int(eval(entry[0])) # this needs to change to 0 when a real attendance dataset is used
	
	w= Walkby(vendor=shop, time=timestamp)
	print 'A walkby by shop ' + shop.name + 'at ' + walkby[0]
	w.save()
	
os.remove('tmp/walkbys.csv')
