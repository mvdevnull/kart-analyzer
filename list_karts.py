#!/usr/bin/python

import re
import MySQLdb
import sys
from config import database
#import time

#User Configuration and Assumptions here


###################
db=MySQLdb.connect(host=database['host'],user=database['user'],passwd=database['pass'], db=database['name'], port=database['port'])
cursor = db.cursor()

#kart_type=250 or rx7?
#kart_num=what kart u want to compare?
kart_type = "rx7"
kart_num = 10

kart_num=raw_input("Which (RX-7) kart do you want to compare?")

print kart_num, "  ", "0.000"
#cursor.execute("""SELECT kart.kart_number, kart.%s from spk.kart where kart.kart_type like '%s' and kart.%s != 0 order by kart.%s""" %\
#(kart_num, kart_type, kart_num, kart_num))
cursor.execute("""SELECT kart.kart_number, kart.%s from spk.kart where kart.%s != 0 order by kart.%s""" %\
(kart_num, kart_num, kart_num))
results = cursor.fetchall()





for row in results:
 print row[0], "  ", row[1]
db.close()
