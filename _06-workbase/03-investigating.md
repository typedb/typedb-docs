---
title: Investigating
keywords:
tags: []
summary: ""
permalink: /docs/workbase/investigating
---

## Investigate
Once we have executed a [Graql query](/docs/query/overview) and visualised its result, we can then investigate each node further to obtain more insights.

<div class="galert">
[Important]
For the purpose of demonstration, we will be interacting with the `phone_calls` keyspace. If you'd like to follow the instructions below step-by-step and see the results accordingly, you need to have modeled the `phone_calls` knowledge graph, loaded its schema into a keyspace and migrated the dataset into it. To do so, follow the [Phone Calls Example](...).
</div>

### Configure Display Settings
Having selected a node, we can choose what colour it should be presented in and what attributes should be displayed on the node.
<div class="slideshow">

[slide:start]
[body:start]![query in one line](/docs/images/workbase/main_settings.png)[body:end]
[footer:start]To configure the display settings, click on the _gear_ icon.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![query in one line](/docs/images/workbase/settings_display.png)[body:end]
[footer:start]Expand the _Display Settings_ section.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![query in one line](/docs/images/workbase/settings_display_type.png)[body:end]
[footer:start]Select the type for which we want to configure the display settings.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/settings_display_label.png)[body:end]
[footer:start]To display or hide an attribute on the nodes of the selected type, we can toggle toggle the attribute of interest. To clear all attributes of the selected type, click on the _eraser_ icon. [footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/settings_display_colour.png)[body:end]
[footer:start]To pick a color for all nodes of the selected type, we need to use the color slider. To reset the color to default, click on the _eraser_ icon.[footer:end]
[slide:end]

</div>

### View Concept Info
<div class="slideshow">

[slide:start]
[body:start]![query in one line](/docs/images/workbase/concept-info.png)[body:end]
[footer:start]To view details about a concept, click on the _info_ icon.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![query in one line](/docs/images/workbase/concept-info_select.png)[body:end]
[footer:start]Select the node of interest by clicking on it.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![query in one line](/docs/images/workbase/concept-info_details.png)[body:end]
[footer:start]View the details of the selected concept.[footer:end]
[slide:end]

</div>

### Visualise Attributes
To visualise the attributes of a node, we first need to select the node by clicking on it and then _hold shift and double click_ on the node.

<div class="galert">
[Note]
The number of attributes to visualise is limited by the _Neighbour Limit_ value configured in the [Query Settings](/docs/workbase/visualising#configure-query-settings).
</div>

### Visualise Neighbours
To visualise neighbours of a node, we first need to select the node by clicking on it and then _double click_ on the node. It's important to note that, the neighbours of a concept vary based on its type.

Neighbours of an entity concept are the **relationships** in which the entity plays a role in.

Neighbours of an attribute concept are the **things** that own it.

Neighbours of a relationship concept are the **things** that play a role in it.

<div class="galert">
[Note]
The number of neighbours to visualise is limited by the _Neighbour Limit_ value configured in the [Query Settings](/docs/workbase/visualising#configure-query-settings).
</div>

### Select Multiple Nodes
To select more than one node, we need to _hold the command/control key_ while clicking on each node of interest.

### Delete a Node
<div class="slideshow">

[slide:start]
[body:start]![query in one line](/docs/images/workbase/delete_select.png)[body:end]
[footer:start]Select one or [multiple nodes](#select-multiple-nodes).[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![query in one line](/docs/images/workbase/delete_right-click.png)[body:end]
[footer:start]Right click on the node.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![query in one line](/docs/images/workbase/delete.png)[body:end]
[footer:start]Select _delete_ from the list.[footer:end]
[slide:end]

</div>