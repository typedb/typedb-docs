---
sidebarTitle: Connection
pageTitle: Configuring Connection
permalink: /docs/workbase/connection
toc: false
---

<!-- 1.5
## Preferences
The preferences panel in Workbase allows us to manage [Keyspaces](/docs/management/keyspace) as well as configuring the connection to the [Grakn Server](/docs/running-grakn/install-and-run#starting-the-grakn-server).

### Configure Connection
<div class="slideshow">

[slide:start]
[header:start][header:end]
[body:start]![Visit KGMS on Google Cloud](/images/workbase/preferences_a.png)[body:end]
[footer:start]Click on the gear icon to open the preferences panel.[footer:end]
[slide:end]

[slide:start]
[header:start][header:end]
[body:start]![Launch](/images/workbase/preferences_b.png)[body:end]
[slide:end]

[slide:start]
[header:start][header:end]
[body:start]![Launch](/images/workbase/preferences_connection_a.png)[body:end]
[footer:start]The top part of the preferences panel allows us to configure the host and port of the running Grakn Server.[footer:end]
[slide:end]

[slide:start]
[header:start][header:end]
[body:start]![Launch](/images/workbase/preferences_connection_b.png)[body:end]
[footer:start]Changing either the host or the port, requires a **Test**.[footer:end]
[slide:end]

[slide:start]
[header:start][header:end]
[body:start]![Launch](/images/workbase/preferences_connection_c.png)[body:end]
[footer:start]If no Grakn Server is running on the given host and port, the connection will be marked as **Invalid**.[footer:end]
[slide:end]

[slide:start]
[header:start][header:end]
[body:start]![Launch](/images/workbase/preferences_connection_a.png)[body:end]
[footer:start]Testing the connection with correct host and port, marks it as **Valid**.[footer:end]
[slide:end]

</div>


### Manage Keyspaces
<div class="slideshow">

[slide:start]
[header:start][header:end]
[body:start]![Visit KGMS on Google Cloud](/images/workbase/preferences_a.png)[body:end]
[footer:start]Click on the gear icon to open the preferences panel.[footer:end]
[slide:end]

[slide:start]
[header:start][header:end]
[body:start]![Launch](/images/workbase/preferences_b.png)[body:end]
[slide:end]

[slide:start]
[header:start][header:end]
[body:start]![Launch](/images/workbase/preferences_keyspaces_a.png)[body:end]
[footer:start]The bottom part of the preferences panel allows us to view, create and delete keyspaces.[footer:end]
[slide:end]

[slide:start]
[header:start][header:end]
[body:start]![Launch](/images/workbase/preferences_keyspaces_b.png)[body:end]
[footer:start]To create a new keyspace, we need to enter a name and click on **Create New Keyspace**.[footer:end]
[slide:end]

[slide:start]
[header:start][header:end]
[body:start]![Launch](/images/workbase/preferences_keyspaces_c.png)[body:end]
[footer:start]This creates the new keyspace and displays it in the list.[footer:end]
[slide:end]

[slide:start]
[header:start][header:end]
[body:start]![Launch](/images/workbase/preferences_keyspaces_d.png)[body:end]
[footer:start]To delete a keyspace, we need to click on the _trash_ icon next to it.[footer:end]
[slide:end]

[slide:start]
[header:start][header:end]
[body:start]![Launch](/images/workbase/preferences_keyspaces_a.png)[body:end]
[footer:start][footer:end]
[slide:end]

</div> -->

## Connect to Grakn
Workbase connects to a running [Grakn Server](/docs/running-grakn/install-and-run#start-the-grakn-server) and interacts with [keyspaces](/docs/management/keyspace). In this short section, we learn how to configure this connection and select a keyspace to interact with.

### Connection
<div class="slideshow">

[slide:start]
[body:start]![Connection](/docs/images/workbase/1.1/connection_1.png)[body:end]
[footer:start]Before running Grakn, you can configure the host and port when you start workbase.[footer:end]
[slide:end]

[slide:start]
[header:start][header:end]
[body:start]![Connection](/docs/images/workbase/1.1/connection_2.png)[body:end]
[footer:start]If Grakn is already running, you may change the configuration by selecting the top right __gear__ icon.[footer:end]
[slide:end]

[slide:start]
[body:start]![Connection](/docs/images/workbase/1.1/connection_3.png)[body:end]
[footer:start]This will show you the preferences panel where you can modify the host and port as per your [custom configuration of Grakn Server](/docs/running-grakn/configuration##host-and-port)[footer:end]
[slide:end]

[slide:start]
[header:start][header:end]
[body:start]![Connection](/docs/images/workbase/1.1/connection_4.png)[body:end]
[footer:start]You may also test your connection to make sure it is valid or not.[footer:end]
[slide:end]


</div>

### Keyspaces
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
[footer:start]To manage your keyspaces click on the top right __gear__ icon to open worbase preferences.[footer:end]
[slide:end]

[slide:start]
[body:start]![Select a Keyspace](/docs/images/workbase/1.1/keyspaces_5.png)[body:end]
[footer:start]The preferences will list all keyspaces. You can type a name and create a new keyspace as above.[footer:end]
[slide:end]

[slide:start]
[body:start]![Select a Keyspace](/docs/images/workbase/1.1/keyspaces_6.png)[body:end]
[footer:start]You may delete an existing keyspace by clicking the __trash__ icon and confirming.[footer:end]
[slide:end]

</div>