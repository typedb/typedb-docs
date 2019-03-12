---
sidebarTitle: Investigation
pageTitle: Investigating Results
permalink: /docs/workbase/investigation
toc: false
---

## Investigate
Once we have executed a [Graql query](/docs/query/overview) and visualised its result, we can then investigate each node further to obtain more insights.

### Configure Display Settings
Having selected a node, we can choose what colour it should be presented in and what attributes should be displayed on the node.
<div class="slideshow">

[slide:start]
[body:start]![query in one line](/docs/images/workbase/1.1.2/investigate_display-settings.png)[body:end]
[footer:start]To configure the display settings, click on the **gear** icon.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![query in one line](/docs/images/workbase/1.1.2/investigate_display-settings-tab.png)[body:end]
[footer:start]Expand the **Display Settings** section.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![query in one line](/docs/images/workbase/1.1.2/investigate_display-settings-select-type.png)[body:end]
[footer:start]Select the type for which we want to configure the display settings.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1.2/investigate_display-settings-select-label.png)[body:end]
[footer:start]To display or hide an attribute on the nodes of the selected type, we can toggle toggle the attribute of interest. To clear all attributes of the selected type, click on the **eraser** icon. [footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1.2/investigate_display-settings-select-colour.png)[body:end]
[footer:start]To pick a color for all nodes of the selected type, we need to use the color slider. To reset the color to default, click on the **eraser** icon.[footer:end]
[slide:end]

</div>

### View Concept Info
<div class="slideshow">

[slide:start]
[body:start]![query in one line](/docs/images/workbase/1.1.2/investigate_info-tab.png)[body:end]
[footer:start]To view details about a concept, click on the **info** icon.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![query in one line](/docs/images/workbase/1.1.2/investigate_info-click-node.png)[body:end]
[footer:start]Select the node of interest by clicking on it.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![query in one line](/docs/images/workbase/1.1.2/investigate_info-node-clicked.png)[body:end]
[footer:start]View the details of the selected concept.[footer:end]
[slide:end]

</div>

### Visualise Attributes
To visualise the attributes of a node, we first need to select the node by clicking on it and then _hold shift and double click_ on the node.

<div class="note">
[Note]
The number of attributes to visualise is limited by the **Neighbour Limit** value configured in the [Query Settings](/docs/workbase/visualising#configure-query-settings).
</div>

### Visualise Neighbours
To visualise neighbours of a node, we first need to select the node by clicking on it and then _double click_ on the node. It's important to note that, the neighbours of a concept vary based on its type.

Neighbours of an entity concept are the **relations** in which the entity plays a role in.

Neighbours of an attribute concept are the **things** that own it.

Neighbours of a relation concept are the **things** that play a role in it.

<div class="note">
[Note]
The number of neighbours to visualise is limited by the **Neighbour Limit** value configured in the [Query Settings](/docs/workbase/visualising#configure-query-settings).
</div>

### Select Multiple Nodes
To select more than one node, we need to **hold the command/control key** while clicking on each node of interest.

### Hide a Node
<div class="slideshow">

[slide:start]
[body:start]![query in one line](/docs/images/workbase/1.1.2/investigate_hide.png)[body:end]
[footer:start]Select one or [multiple nodes](#select-multiple-nodes).[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![query in one line](/docs/images/workbase/1.1.2/investigate_hide-right-click.png)[body:end]
[footer:start]Right click on the node.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![query in one line](/docs/images/workbase/1.1.2/investigate_hide-click.png)[body:end]
[footer:start]Select **hide** from the list.[footer:end]
[slide:end]

</div>