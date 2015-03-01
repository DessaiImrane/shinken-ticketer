#!/usr/bin/env python

# ticketer.py
# Shinken command script for generating ServiceNow Incidents via the REST API
import getopt
import json
import sqlite3
import sys
import os

# Determine current working directory and set database path
cwd = os.path.dirname(os.path.realpath(__file__))
dbpath = cwd + '/data/incident.db'

# Read credentials for accessing ServiceNow REST API
with open('credentials.json') as data_file:    
  data = json.load(data_file)
data_file.close()

def main(argv):
  # Initialize/Preallocate list to hold alarm details
  alarm = ['type','host','addr','srvc','output','desc'] 

  try:
    opts, args = getopt.getopt(argv,"h", ["help", "type=", "host=", "addr=",
    "srvc=", "output=", "desc=", "initdb"])
  except getopt.GetoptError as err:          
    print(err)
    usage()                         
    sys.exit(2)

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
    elif opt == '--desc':
      alarm[4] = arg
    elif opt == '--output':
      alarm[5] = arg
    elif opt == '--state':
      srvcState = arg
    elif opt == '--initdb':
      initdb()
  # Generate new ticket if this is a new alarm
  if alarm[0] == 'PROBLEM':
    create(alarm)
  # Resolve existing ticket if the alarm has recovered
  elif alarm[0] == 'RECOVERY':
    resolve(alarm)

# Print usage, even though this is called by a daemon?
def usage():
  print("Usage: ticketer.py --host --addr --service --output --desc")

# Setup sqlite database
def initdb():
  print("INIT THAT DB YO!")
  sql = '''
        CREATE TABLE IF NOT EXISTS
          data(id INTEGER PRIMARY KEY,
          date DATETIME,
          type TEXT,
          host TEXT,
          addr TEXT,
          res INT)'''
  db = sqlite3.connect(dbpath)
  cursor = db.cursor()
  cursor.execute(sql)
  db.commit()
  db.close()

# Add new incident record to database
def dbAdd(ticketInfo):
  print("Adding new record to DB %s" % ticketInfo)

# Delete resolved incident record from database
def dbDel(ticketInfo):
  print("Removing record from DB")

# Create new ticket in Service Now
def create(alarm):
  print("Creating ticket for %s" % alarm)
  ticketInfo = 'INC31337'
  dbAdd(ticketInfo)

# Delete record from database when alarm clears
def resolve(alarm):
  print("Resolving ticket and removing entry for %s" % alarm[1:])
if __name__ == "__main__":
  main(sys.argv[1:])
