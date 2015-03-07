Shinken Ticketer
======

* Creates new incident tickets in ServiceNow for Shinken alarms.

* Utilizes a sqlite database for ticket tracking.

* Resolves incidents and removes ticket info from database when alarm clears.

* Doesn't actually work yet.

Installation:
###

Clone repo to Shinken installation directory:

  $ git clone http://github.com/mikeder/shinken-ticketer

Set script as executable:

  $ chmod +x ticketer.py

Create symlink for calling script:

  $ ln -s /shinken-ticketer/ticketer.py /usr/bin/ticketer


Shinken Command to use this script:

```
define command {
    command_name    ticketer
    command_line    /usr/bin/ticketer --type $NOTIFICATIONTYPE$ --host
    $HOSTNAME$ --addr $HOSTADDRESS$ --srvc $SERVICEDESC --output
    $SERVICEOUTPUT$ --state $SERVICESTATE$
  }
```

TODO:
###

* Daemonize script

* Integrate web.py to accept http requests so Shinken command can be reduced
to a curl command.

* Add a list of mission critical systems, if they experience a problem alert
set impact/urgency of ticket higher (P2)
