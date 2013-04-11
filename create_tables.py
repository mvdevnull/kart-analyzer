#!/usr/bin/python

import MySQLdb
from config import database

db=MySQLdb.connect(host=database['host'],user=database['user'],passwd=database['pass'], db=database['name'], port=database['port'])
cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS driver
	(
	driver_name text,
	driver_cust_id text
	)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS heat
	(
	heat_num int,
	heat_num_plus_custid text,
	heat_driver_custid text,
	heat_driver_kart text,
	heat_driver_fastlap float,
	heat_datetime datetime,
	heat_driver_place text,
	heat_driver_name text,
	heat_type text,
	weight_rain text
	)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS kart
	(
	kart_number text
	)""")