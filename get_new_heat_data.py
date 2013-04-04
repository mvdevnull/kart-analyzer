#!/usr/bin/python

from bs4 import BeautifulSoup
import urllib2
import re
import MySQLdb
import sys

DATABASE_HOST = "localhost"
DATABASE_USER = "spk"
DATABASE_NAME = "spk"
DATABASE_PASSWD = "spk"
DATABASE_PORT = 3306



db=MySQLdb.connect(host=DATABASE_HOST,user=DATABASE_USER,passwd=DATABASE_PASSWD, db=DATABASE_NAME, port=int(DATABASE_PORT))
cursor = db.cursor()
cursor.execute("""SELECT driver_name, driver_cust_id FROM driver""")
results = cursor.fetchall()
for row in results:
 driver_name = row[0]
 driver_number = row[1]
 driver_number_int = "%s" % (driver_number)
 #print "Processing new heats for Driver:", driver_name
 url = urllib2.urlopen("http://www.clubspeedtiming.com/spwvirginia/RacerHistory.aspx?CustID=%s" % \
 (driver_number))
 soup = BeautifulSoup(url)
 href_filter = soup.select("[class~=Normal]")

 for heat_all in href_filter:
  heat_str = str(heat_all)  #may not be needed?
  heat_num = re.search('(?<=\=)\d+', heat_str)
  kart_num = re.search('(?<=art.)\d+', heat_str)
  fastlap = re.findall('(?<=td width\=\"10...)\d+\.?\d*', heat_str)
  heat_num_plus_custid_list = heat_num.group(0),driver_number_int
  heat_num_plus_custid_int = int(''.join(map(str,heat_num_plus_custid_list)))
  #DATETIME
  heat_datetime = re.split("\n+", heat_str)
  heat_datetime = heat_datetime[2]
  heat_datetime = heat_datetime.lstrip('\t')
  heat_datetime_month = re.split("\/+", heat_datetime)
  heat_datetime_day = heat_datetime_month[1]
  heat_datetime_year = heat_datetime_month[2]
  heat_datetime_month = heat_datetime_month[0]
  heat_datetime_year = re.split(" ", heat_datetime_year)
  heat_datetime_time = heat_datetime_year[1]
  heat_datetime_time = re.split("\:", heat_datetime_time)
  heat_datetime_hour = heat_datetime_time[0]
  heat_datetime_min = heat_datetime_time[1]
  heat_datetime_sec = "00"
  heat_datetime_xm = heat_datetime_year[2]
  if "PM" in heat_datetime_xm:
   if int(heat_datetime_hour) <> 12:
    heat_datetime_hour = int(heat_datetime_hour) + 12
   else:
    pass
  else:
   pass
  heat_datetime_time = str(heat_datetime_hour) + ":" + str(heat_datetime_min) + ":" + str(heat_datetime_sec)
  heat_datetime_year = heat_datetime_year[0]
  heat_datetime = heat_datetime_year + "-" + heat_datetime_month + "-" + heat_datetime_day + " " + heat_datetime_time

  #DRIVER POSISTION
  heat_place = re.split("\n+", heat_str)
  heat_place = heat_place[4]
  heat_place = heat_place.lstrip('\t')
  heat_place = re.findall(r"(\d+)", heat_place)
  heat_place = heat_place[0]

  #HEAT TYPE
  #heat_type = re.split("n+", heat_str)
  heat_type = re.search('(?<=\=)\d+..+\-', heat_str)
  heat_type = heat_type.group(0)
  heat_type_split = re.split("\>+", heat_type)
  heat_type_right = heat_type_split[1]
  heat_type = heat_type_right
  #sys.exit()
  ##################################################################

  try:
   cursor.execute ("""
        INSERT into heat (heat_num_plus_custid) \
        VALUES ('%d')""" % \
        (heat_num_plus_custid_int))
   db.commit()

  except:
   db.rollback()
   #print 'Skipping  - Racer', driver_name, 'in heat', heat_num.group(0)

  else:
   print 'Updating - Driver', driver_name, 'in heat', heat_num.group(0), 'at', heat_datetime, 'kart#', kart_num.group(0), 'fast lap', fastlap[1], 'heat place', heat_place
   cursor.execute ("""
        UPDATE spk.heat SET heat.heat_num = %s
        WHERE heat.heat_num_plus_custid = %s
        """ %\
        (heat_num.group(0),heat_num_plus_custid_int))
   db.commit()

   cursor.execute ("""
        UPDATE spk.heat SET heat.heat_driver_name = '%s'
        WHERE heat.heat_num_plus_custid = %s
        """ %\
        (driver_name, heat_num_plus_custid_int))
   db.commit()

   cursor.execute ("""
        UPDATE spk.heat SET heat.heat_driver_custid = '%s'
        WHERE heat.heat_num_plus_custid = %s
        """ %\
        (driver_number_int, heat_num_plus_custid_int))
   db.commit()

   cursor.execute ("""
        UPDATE spk.heat SET heat.heat_driver_kart = '%s'
        WHERE heat.heat_num_plus_custid = %s
        """ %\
        (kart_num.group(0), heat_num_plus_custid_int))
   db.commit()

   cursor.execute ("""
        UPDATE spk.heat SET heat.heat_driver_fastlap = '%s'
        WHERE heat.heat_num_plus_custid = %s
        """ %\
        (fastlap[1], heat_num_plus_custid_int))
   db.commit()

   cursor.execute ("""
        UPDATE spk.heat SET heat.heat_datetime = '%s'
        WHERE heat.heat_num_plus_custid = %s
        """ %\
        (heat_datetime, heat_num_plus_custid_int))
   db.commit()

   cursor.execute ("""
        UPDATE spk.heat SET heat.heat_driver_place = '%s'
        WHERE heat.heat_num_plus_custid = %s
       """ %\
        (heat_place, heat_num_plus_custid_int))
   db.commit()

   cursor.execute ("""
        UPDATE spk.heat SET heat.heat_type = '%s'
        WHERE heat.heat_num_plus_custid = %s
        """ %\
        (heat_type, heat_num_plus_custid_int))
   db.commit()


db.close()

print "\nComplete"
