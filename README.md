Shinken Ticketer
======

* Creates new incident tickets in ServiceNow for Shinken alarms.

* Utilizes a sqlite database for ticket tracking.

* Resolves incidents and removes ticket info from database when alarm clears.

* Doesn't actually work yet.

Installation:
####

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
####

* Finish ticket generation function (some fields do not populate correctly)
* Add a list of mission critical systems, if they experience a problem alert set impact/urgency of ticket higher (P2)
* Build ticket resolution function
* Add comment with URL to shinken web ui
* Handle recovery
* What about flapping ?
*	Auto Init DB if not exists
