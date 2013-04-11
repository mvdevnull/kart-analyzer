#!/usr/bin/python

import re
import MySQLdb
import sys
from config import database
#import time

#User Configuration and Assumptions here

min_date = "2013-03-01 00:00:00"
weight_factor = .1
heat_diff_max = 4

###################

db=MySQLdb.connect(host=database['host'],user=database['user'],passwd=database['pass'], db=database['name'], port=database['port'])
cursor = db.cursor()
cursor.execute("""SELECT min(heat_num) as heat_num from heat where heat_datetime >= '%s'""" %\
(min_date))
results = cursor.fetchall()
for row in results:
 min_heat = row[0]

cursor.execute("""SELECT max(heat_num) as heat_num from heat""")
results = cursor.fetchall()
for row in results:
 last_heat = row[0]

print "============================================"
print "*ASSUMPTION #1 -", min_date, "Heats (from ", min_heat, "to", last_heat,")"
print "*ASSUMPTION #2 - same driver must drive different kart within", heat_diff_max, "number of heats"
print "*ASSUMPTION #3 - When two differing data points exists between two karts, the newer number affects the final time with a weighted modification of", weight_factor
print "*ASSUMPTION #4 - Exclude heats where karts are weighted (ie: *league*)"
print "============================================"

print "...Zeroing all previous kart data"
cursor.execute("""SELECT DISTINCT kart_number from spk.kart order by kart_number """)
results = cursor.fetchall()
for row in results:
 kartnum_cur = row[0]
 cursor.execute ("""
        UPDATE spk.kart SET kart.%s = '0'
        """ %\
        (kartnum_cur))
 db.commit()

#ASSUMPTION# 1 & 4
cursor.execute("""SELECT heat_driver_kart, heat_driver_fastlap, heat_num, heat_driver_name from spk.heat where heat_num > %s and heat_type not like '%%nduro%%' and heat_type not like '%%kid
s%%'
and heat_type not like '%%league%%' or heat_type not like '%%race%%'
and weight_rain != 1 order by heat_driver_name, heat_num""" %\
(min_heat))
results = cursor.fetchall()
row_lastzero = 1
row_lastone = 1
row_lasttwo = 1
row_lastthree = 1
for row in results:
 #print row[0], row[1], row[2], row[3]
 if row[3] == row_lastthree:
  heat_diff = row[2] - row_lasttwo
  if row[0] != row_lastzero:
   #ASSUMPTION#2
   if heat_diff < heat_diff_max:
    #ASSUMPTION#3
    karttime_cur = row[1]
    karttime_last = row_lastone
    kartnum_cur = row[0]
    kartnum_last = row_lastzero
    kart1diff = karttime_cur - karttime_last
    kart1diff_neg = -kart1diff
    print "+RAW [", row[3], "]- kart", kartnum_last, "is", kart1diff, "[+faster/-slower] than kart", kartnum_cur
    try:
      cursor.execute ("""UPDATE spk.kart SET kart.%s = '%s' WHERE kart.kart_number = %s""" %\
      (kartnum_last, kart1diff, kartnum_cur))
    except:
      query = "ALTER TABLE spk.kart ADD kart.%s text" % (kartnum_last)
      cursor.execute (query)
      cursor.execute ("""UPDATE spk.kart SET kart.%s = '%s' WHERE kart.kart_number = %s""" %\
      (kartnum_last, kart1diff, kartnum_cur))
    db.commit()
    try:
      cursor.execute ("""UPDATE spk.kart SET kart.%s = '%s' WHERE kart.kart_number = %s""" %\
      (kartnum_cur, kart1diff_neg, kartnum_last))
    except:
      query = "ALTER TABLE spk.kart ADD kart.%s text" % (kartnum_cur)
      cursor.execute (query)      
    db.commit()
   else:
    pass
  else:
   pass
 else:
  pass
 row_lastzero = row[0]
 row_lastone = row[1]
 row_lasttwo = row[2]
 row_lastthree = row[3]

###########
#now cycle through all karts and find relational inferences
cursor.execute("""SELECT DISTINCT kart_number from spk.kart order by kart_number """)
results = cursor.fetchall()
#Cycle Through All kart #'s
for row in results:
 #print "cycling through kart", row[0]
 kartnum_cur_x = row[0]
 cursor.execute("""SELECT DISTINCT kart_number from spk.kart order by kart_number """)
 results = cursor.fetchall()
 for row in results:
  kartnum_cur_y = row[0]
  cursor.execute("""SELECT spk.kart.%s from spk.kart where kart_number = %s""" %\
  (kartnum_cur_y, kartnum_cur_x))
  diff = cursor.fetchone()
  diff = diff[0]
  if diff != 0:
   cursor.execute("""SELECT spk.kart.kart_number, spk.kart.%s from spk.kart where spk.kart.%s <> 0 and spk.kart.kart_number <> %s""" %\
   (kartnum_cur_y, kartnum_cur_y, kartnum_cur_x))
   results = cursor.fetchall()
   for row in results:
    #print "While cycling through kart", kartnum_cur_x, "found update required with kart", row[0]
    diff1 = -row[1]
    cursor.execute("""SELECT spk.kart.%s from spk.kart where kart_number = %s""" %\
    (kartnum_cur_x, kartnum_cur_y))
    diff2 = cursor.fetchone()
    diff2 = diff2[0]
    newdiff = -diff2 + diff1
    newdiff_neg = -newdiff
    kartnum_cur_z = row[0]
    #Check if data exists already, no data - update & data exists - weight it in
    cursor.execute("""SELECT spk.kart.%s from spk.kart where kart_number = %s""" % (kartnum_cur_z, kartnum_cur_x))
    data_exists = cursor.fetchone()
    data_exists = data_exists[0]
    if data_exists == 0:
     cursor.execute("""UPDATE spk.kart SET spk.kart.%s = '%s' WHERE spk.kart.kart_number = %s""" % (kartnum_cur_z, newdiff, kartnum_cur_x))
     db.commit()
     cursor.execute("""UPDATE spk.kart SET spk.kart.%s = '%s' WHERE spk.kart.kart_number = %s""" % (kartnum_cur_x, newdiff_neg, kartnum_cur_z))
     db.commit()
     print "+IMPLIED - kart", kartnum_cur_z, "is", newdiff, "[+faster/-slower] than kart", kartnum_cur_x
     #print "(Given difference of", kartnum_cur_z, "and", kartnum_cur_y,  "is", diff1, "and kart", kartnum_cur_x, "and", kartnum_cur_y, "is", diff2, ")"
    else:
     #Data already exists, so carefully smooth in the factor by some factor
     newdiffsmooth = float(str(newdiff)) * weight_factor
     weight_factor_neg = 1-weight_factor
     olddiffsmooth = float(str(data_exists)) * weight_factor_neg
     newdiffsmooth2 = float(str(newdiffsmooth)) + float(str(olddiffsmooth))
     newdiffsmooth2 = round(newdiffsmooth2,3)
     newdiffsmooth2_neg = -newdiffsmooth2
     if data_exists == newdiff:
      #print "+WEIGHTED (skip same)", data_exists, "vs", newdiff
      pass
     else:
      print "+WEIGHTED - kart", kartnum_cur_z, "and", kartnum_cur_x, "difference of old number", data_exists, "and new number", newdiff, "will be replaced with", newdiffsmooth2

      #Update weighted new number
      cursor.execute ("""UPDATE spk.kart SET kart.%s = '%s' WHERE kart.kart_number = %s""" %\
      (kartnum_cur_z, newdiffsmooth2, kartnum_cur_x))
      db.commit()
      cursor.execute ("""UPDATE spk.kart SET kart.%s = '%s' WHERE kart.kart_number = %s""" %\
      (kartnum_cur_x, newdiffsmooth2_neg, kartnum_cur_z))
      db.commit()

  else:
   pass

db.close()

print "Complete"

