---
sidebarTitle: Connection
pageTitle: Configuring Connection
permalink: /docs/workbase/connection
toc: false
---

## Connect to Grakn
Workbase connects to a running [Grakn Server](/docs/running-grakn/install-and-run#start-the-grakn-server) and interacts with [keyspaces](/docs/management/keyspace). In this short section, we learn how to configure this connection and select a keyspace to interact with.

### Start Workbase for Grakn Core
<div class="slideshow">

[slide:start]
[body:start]![Connection](/docs/images/workbase/1.1.2/preferences_core-login.png)[body:end]
[footer:start]We can specify the host and port when we start workbase.[footer:end]
[slide:end]

</div>

### Start Workbase for Grakn KGMS [KGMS ONLY]
<div class="slideshow">

[slide:start]
[body:start]![Connection](/docs/images/workbase/1.1.2/preferences_kgms-login.png)[body:end]
[footer:start]We can specify the host, port, username and password when we start workbase.[footer:end]
[slide:end]

</div>

### Configure Connection
<div class="slideshow">

[slide:start]
[header:start][header:end]
[body:start]![Connection](/docs/images/workbase/1.1.2/preferences_configure_open-preferences.png)[body:end]
[footer:start]If Grakn is already running, we may change the configuration by selecting the top right **gear** icon.[footer:end]
[slide:end]

[slide:start]
[body:start]![Connection](/docs/images/workbase/1.1.2/preferences_configure-host-port.png)[body:end]
[footer:start]This will show us the preferences panel where we can modify the host and port as per our [custom configuration of Grakn Server](/docs/running-grakn/configuration##host-and-port)[footer:end]
[slide:end]

[slide:start]
[header:start][header:end]
[body:start]![Connection](/docs/images/workbase/1.1.2/preferences_test-connection.png)[body:end]
[footer:start]We may also test our connection to make sure it is valid.[footer:end]
[slide:end]

</div>


### Select A Keyspace
<div class="slideshow">

[slide:start]
[body:start]![Select a Keyspace](/docs/images/workbase/1.1.2/preferences_select-keyspace.png)[body:end]
[footer:start]To select a **keyspace** for Workbase to connect to, we need to click on the keyspace button.[footer:end]
[slide:end]

[slide:start]
[body:start]![Select a Keyspace](/docs/images/workbase/1.1.2/preferences_list-keyspaces.png)[body:end]
[footer:start]This shows us the list of all keyspaces running on the Grakn Server. We then select the keyspace of interest.[footer:end]
[slide:end]

[slide:start]
[body:start]![Select a Keyspace](/docs/images/workbase/1.1.2/preferences_keyspace-selected.png)[body:end]
[footer:start]Keyspace is now connected to the selected keyspace, in our case that is named `social_network`.[footer:end]
[slide:end]

</div>

### Manage Keyspaces
<div class="slideshow">

[slide:start]
[body:start]![Select a Keyspace](/docs/images/workbase/1.1.2/preferences_open-preferences.png)[body:end]
[footer:start]To manage our keyspaces click on the top right **gear** icon to open worbase preferences.[footer:end]
[slide:end]

[slide:start]
[body:start]![Select a Keyspace](/docs/images/workbase/1.1.2/preferences_create-keyspace.png)[body:end]
[footer:start]The preferences will list all keyspaces. We can type a name and click on **Create New Keyspace**.[footer:end]
[slide:end]

[slide:start]
[body:start]![Select a Keyspace](/docs/images/workbase/1.1.2/preferences_delete-keyspace.png)[body:end]
[footer:start]We may delete an existing keyspace by clicking the **trash** icon and confirming.[footer:end]
[slide:end]

</div>