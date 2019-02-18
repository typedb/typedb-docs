---
sidebarTitle: Connection
pageTitle: Configuring Connection
permalink: /docs/workbase/connection
toc: false
---

## Connect to Grakn
Workbase connects to a running [Grakn Server](/docs/running-grakn/install-and-run#start-the-grakn-server) and interacts with [keyspaces](/docs/management/keyspace). In this short section, we learn how to configure this connection and select a keyspace to interact with.

### Connection
<div class="slideshow">

[slide:start]
[body:start]![Connection](/docs/images/workbase/1.1/connection_1.png)[body:end]
[footer:start]Before running Grakn, we can configure the host and port when we start workbase.[footer:end]
[slide:end]

[slide:start]
[header:start][header:end]
[body:start]![Connection](/docs/images/workbase/1.1/connection_2.png)[body:end]
[footer:start]If Grakn is already running, we may change the configuration by selecting the top right __gear__ icon.[footer:end]
[slide:end]

[slide:start]
[body:start]![Connection](/docs/images/workbase/1.1/connection_3.png)[body:end]
[footer:start]This will show us the preferences panel where we can modify the host and port as per our [custom configuration of Grakn Server](/docs/running-grakn/configuration##host-and-port)[footer:end]
[slide:end]

[slide:start]
[header:start][header:end]
[body:start]![Connection](/docs/images/workbase/1.1/connection_4.png)[body:end]
[footer:start]We may also test our connection to make sure it is valid or not.[footer:end]
[slide:end]


</div>

### Manage Keyspaces
<div class="slideshow">

[slide:start]
[body:start]![Select a Keyspace](/docs/images/workbase/1.1/keyspaces_1.png)[body:end]
[footer:start]To select a keyspace for Workbase to connect to, we need to click on the keyspace button.[footer:end]
[slide:end]

[slide:start]
[body:start]![Select a Keyspace](/docs/images/workbase/1.1/keyspaces_2.png)[body:end]
[footer:start]This shows us the list of all keyspaces running on the Grakn Server. We then select the keyspace of interest.[footer:end]
[slide:end]

[slide:start]
[body:start]![Select a Keyspace](/docs/images/workbase/1.1/keyspaces_3.png)[body:end]
[footer:start]Keyspace is now connected to the selected keyspace, in our case that is named `social_network`.[footer:end]
[slide:end]

[slide:start]
[body:start]![Select a Keyspace](/docs/images/workbase/1.1/keyspaces_4.png)[body:end]
[footer:start]To manage our keyspaces click on the top right __gear__ icon to open worbase preferences.[footer:end]
[slide:end]

[slide:start]
[body:start]![Select a Keyspace](/docs/images/workbase/1.1/keyspaces_5.png)[body:end]
[footer:start]The preferences will list all keyspaces. We can type a name and create a new keyspace as above.[footer:end]
[slide:end]

[slide:start]
[body:start]![Select a Keyspace](/docs/images/workbase/1.1/keyspaces_6.png)[body:end]
[footer:start]We may delete an existing keyspace by clicking the __trash__ icon and confirming.[footer:end]
[slide:end]

</div>