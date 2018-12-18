---
title: Configuring Connection
keywords:
tags: []
summary: ""
permalink: /docs/workbase/connection
---

<!-- 1.5
## Preferences
The preferences panel in Workbase allows us to manage [Keyspaces](/docs/management/keyspace) as well as configuring the connection to the [Grakn Server](/docs/running-grakn/install-n-run#starting-the-grakn-server).

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
Workbase connects to a running [Grakn Server](/docs/running-grakn/install-n-run#starting-a-grakn-server) and interacts with [keyspaces](/docs/management/keyspace). In this short section, we will learn how to configure this connection and select a keyspace to interact with.

### Specify the host and port
<div class="slideshow">

[slide:start]
[body:start]![Specify the host and port](/docs/images/workbase/main_settings.png)[body:end]
[footer:start]Right after opening the Workbase, click on the _gear_ icon in the right sidebar.[footer:end]
[slide:end]

[slide:start]
[header:start][header:end]
[body:start]![Specify the host and port](/docs/images/workbase/settings_connection.png)[body:end]
[footer:start]Under _Connection Settings_ , alter the host and port as per your [custom configuration of Grakn Server](/docs/running-grakn/configuration##host-and-port).[footer:end]
[slide:end]

</div>

### Select a Keyspace
<div class="slideshow">

[slide:start]
[body:start]![Select a Keyspace](/docs/images/workbase/main_keyspace.png)[body:end]
[footer:start]To select a keyspace for Workbase to connect to, we need to click on the keyspace button.[footer:end]
[slide:end]

[slide:start]
[body:start]![Select a Keyspace](/docs/images/workbase/main_keyspace_select.png)[body:end]
[footer:start]This shows us the list of all keyspaces running on the Grakn Server. We then select the keyspace of interest.[footer:end]
[slide:end]

[slide:start]
[body:start]![Select a Keyspace](/docs/images/workbase/main_keyspace_selected.png)[body:end]
[footer:start]Keyspace is now connected to the selected keyspace, in our case that is named `phone_calls`.[footer:end]
[slide:end]

</div>