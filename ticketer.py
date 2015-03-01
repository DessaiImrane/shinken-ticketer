#!/usr/bin/env python

# ticketer.py
# Shinken command script for generating ServiceNow Incidents via the REST API
import datetime
import getopt
import json
import sqlite3
import sys
import os
import requests

# Determine current working directory and set database path
cwd = os.path.dirname(os.path.realpath(__file__))
dbpath = cwd + '/data/incident.db'

# Read credentials for accessing ServiceNow REST API
with open('credentials.json') as data_file:    
  sn_data = json.load(data_file)
data_file.close()

def main(argv):
  # Initialize/Preallocate list to hold alarm details
  alarm = ['type','host','addr','srvc','output','state'] 

  try:
    opts, args = getopt.getopt(argv,"h", ["help", "type=", "host=", "addr=",
    "srvc=", "output=", "state=", "initdb"])
  except getopt.GetoptError as err:          
    print(err)
    usage()                         
    sys.exit(2)
  # If no options are given, print usage
  if not opts:
    usage()
  # Handle all the options and arguments passed in
  for opt, arg in opts:
    if opt in ("-h", "--help"):
      usage()
      sys.exit()
    elif opt == '--type':
      alarm[0] = arg
    elif opt == '--host':
      alarm[1] = arg
    elif opt == '--addr':
      alarm[2] = arg
    elif opt == '--srvc':
      alarm[3] = arg
    elif opt == '--output':
      alarm[4] = arg
    elif opt == '--state':
      alarm[5] = arg
    elif opt == '--initdb':
      initdb()
  # Generate new ticket if this is a new alarm
  if alarm[0] == 'PROBLEM':
    createInc(alarm)
  # Resolve existing ticket if the alarm has recovered
  elif alarm[0] == 'RECOVERY':
    resolveInc(alarm)

# Print usage, even though this is called by a daemon?
def usage():
  print("Usage: ticketer.py --type --host --addr --srvc --output --state")
  print("--type $NOTIFICATIONTYPE$")
  print("--host $HOSTNAME$")
  print("--addr $HOSTADDRESS$")
  print("--srvc $SERVICEDESC$")
  print("--output $SERVICEOUTPUT$")
  print("--state $SERVICESTATE$")

# Setup sqlite database
def initdb():
  sql = '''
        CREATE TABLE IF NOT EXISTS
          incident(id INTEGER PRIMARY KEY,
          date DATETIME,
          sysid TEXT,
          host TEXT,
          srvc TEXT)'''
  db = sqlite3.connect(dbpath)
  cursor = db.cursor()
  cursor.execute(sql)
  db.commit()
  db.close()
  print("Database successfully created.")

# Add new incident record to database
def dbAdd(sysid,host,srvc):
  date = datetime.datetime.now()
  sql = '''
        INSERT INTO incident(date, sysid, host, srvc)
        VALUES(?,?,?,?)'''
  values = [(date,sysid,host,srvc)]
  db = sqlite3.connect(dbpath)
  cursor = db.cursor()
  cursor.executemany(sql,values)
  db.commit()
  db.close()
  print('New record added to database.')

# Lookup an incident record in the database and pass ID to dbDel()
def dbLookup(host,srvc):
  # CHANGE id TO sysid ONCE RECORDS ARE GETTING POPULATED
  sql = '''
        SELECT sysid FROM incident WHERE host = ? AND srvc = ?''' 
  db = sqlite3.connect(dbpath)
  db.text_factory = str
  cursor = db.cursor()
  values = [(host,srvc)]
  print(values)
  cursor.execute(sql,(host,srvc))
  sysid = cursor.fetchone()
  db.close()
  return sysid

# Delete resolved incident record from database
def dbDel(sysid):
  sql = '''
        DELETE FROM incident WHERE sysid = ?'''
  db = sqlite3.connect(dbpath)
  cursor = db.cursor()
  try:
    cursor.execute(sql,sysid)
    db.commit()
    db.close()
    print("Record deleted")
  except Exception as err:
    print('\033[1;91mThere was an error while deleting the record\033[1;m')
    print('\033[1;91m%s\033[1;m' % err)
    pass

# Create new ticket in Service Now
def createInc(alarm):
  print("Creating ticket for %s" % alarm)
  ### Insert call to SN API here and grab sysid from response body
  sysid = '2nk20912kl32u109312'
  host = alarm[1]
  srvc = alarm[3]
  dbAdd(sysid,host,srvc)

# Resolve incident when alarm has cleared
def resolveInc(alarm):
  host = alarm[1]
  srvc = alarm[3]
  sysid = dbLookup(host,srvc)
  if not sysid:
    print("No record found, nothing to resolve")
  else:
    print("Resolving ticket and removing entry for %s" % sysid)
    dbDel(sysid)

if __name__ == "__main__":
  main(sys.argv[1:])
