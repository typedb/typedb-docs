---
pageTitle: Configuring Connection
keywords: grakn, workbase, workbase preferences
longTailKeywords: grakn workbase preferences, grakn workbase connection, grakn workbase manage databases
Summary: Working with the preferences panel in Grakn Workbase.
toc: false
---

## Connect to Grakn
Workbase connects to a running [Grakn Server](/docs/running-grakn/install-and-run#start-the-grakn-server) and interacts with [databases](../06-management/01-database.md). In this short section, we learn how to configure this connection and select a database to interact with.

### Start Workbase for Grakn Core

![Connection](/docs/images/workbase/preferences_core-login.png)
[caption: We can specify the host and port when we start workbase.]


### Start Workbase for Grakn Cluster [Cluster ONLY]

![Connection](/docs/images/workbase/preferences_cluster-login.png)
[caption: We can specify the host, port, username and password when we start workbase.]


### Configure Connection
<div class="slideshow">

[slide:start]
[header:start][header:end]
[body:start]![Connection](/docs/images/workbase/preferences_configure_open-preferences.png)[body:end]
[footer:start]If Grakn is already running, we may change the configuration by selecting the top right **gear** icon.[footer:end]
[slide:end]

[slide:start]
[body:start]![Connection](/docs/images/workbase/preferences_configure-host-port.png)[body:end]
[footer:start]This will show us the preferences panel where we can modify the host and port as per our [custom configuration of Grakn Server](/docs/running-grakn/configuration##host-and-port)[footer:end]
[slide:end]

[slide:start]
[header:start][header:end]
[body:start]![Connection](/docs/images/workbase/preferences_test-connection.png)[body:end]
[footer:start]We may also test our connection to make sure it is valid.[footer:end]
[slide:end]

</div>


### Select A Database
<div class="slideshow">

[slide:start]
[body:start]![Select a Database](/docs/images/workbase/preferences_select-database.png)[body:end]
[footer:start]To select a **database** for Workbase to connect to, we need to click on the database button.[footer:end]
[slide:end]

[slide:start]
[body:start]![Select a Database](/docs/images/workbase/preferences_list-databases.png)[body:end]
[footer:start]This shows us the list of all databases running on the Grakn Server. We then select the database of interest.[footer:end]
[slide:end]

[slide:start]
[body:start]![Select a Database](/docs/images/workbase/preferences_database-selected.png)[body:end]
[footer:start]Database is now connected to the selected database, in our case that is named `social_network`.[footer:end]
[slide:end]

</div>

### Manage Databases
<div class="slideshow">

[slide:start]
[body:start]![Select a Database](/docs/images/workbase/preferences_open-preferences.png)[body:end]
[footer:start]To manage our databases click on the top right **gear** icon to open worbase preferences.[footer:end]
[slide:end]

[slide:start]
[body:start]![Select a Database](/docs/images/workbase/preferences_create-database.png)[body:end]
[footer:start]The preferences will list all databases. We can type a name and click on **Create New Database**.[footer:end]
[slide:end]

[slide:start]
[body:start]![Select a Database](/docs/images/workbase/preferences_delete-database.png)[body:end]
[footer:start]We may delete an existing database by clicking the **trash** icon and confirming.[footer:end]
[slide:end]

</div>