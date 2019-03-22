---
pageTitle: Visualising Results
keywords: grakn, workbase, visualisation
longTailKeywords: grakn visualise graph, visualise grakn, visualise grakn graph, workbase visualisation, grakn visualize graph, visualize grakn, visualize grakn graph, workbase visualization
Summary: Using Workbase to visualise a Grakn Knowledge Graph.
toc: false
permalink: /docs/workbase/visualisation
---

## Visualise
Workbase allows visualisation of answers returned by [Graql queries](/docs/query/overview). These include _custom_ and _pre-defined type-based_ queries.

### Execute Custom Queries
<div class="slideshow">

[slide:start]
[body:start]![Graql editor](/docs/images/workbase/1.1.1/visualise_graql-editor.png)[body:end]
[footer:start][Having selected the keyspace](/docs/workbase/preferences#selecting-a-keyspace), we can write queries of our own in the Graql Editor.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![query in one line](/docs/images/workbase/1.1.1/visualise_graql-editor-custom.png)[body:end]
[footer:start]We can write queries in one single line.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1.1/visualise_graql-editor-multiline.png)[body:end]
[footer:start]Or in multiple lines by _holding shift and pressing enter_.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1.1/visualise_graql-editor-play.png)[body:end]
[footer:start]To run the query, we need to press the **execute** button.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1.1/visualise_graql-editor-response.png)[body:end]
[footer:start]Executing a query visualises the result.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1.1/visualise_graql-editor-clear.png)[body:end]
[footer:start]To clear the results, we need to click on the **refresh** button.[footer:end]
[slide:end]
<!-- -->
[slide:start]

[body:start]![Launch](/docs/images/workbase/1.1.1/visualise_graql-editor-minimise.png)[body:end]
[footer:start]We can also minimise the Graql Editor to focus on the visualised results.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1.1/visualise_graql-editor-clear-editor.png)[body:end]
[footer:start]To clear the the Graql Editor, we need to click on the **delete** button.[footer:end]
[slide:end]
</div>

### Execute Type-based Queries
<div class="slideshow">

[slide:start]
[body:start]![Graql editor](/docs/images/workbase/1.1.1/visualise_types.png)[body:end]
[footer:start][Having selected the keyspace](/docs/workbase/preferences#selecting-a-keyspace), we can explore the [Concept Types](/docs/schema/concepts) as defined in the [schema](/docs/schema/overview).[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![query in one line](/docs/images/workbase/1.1.1/visualise_types-opened.png)[body:end]
[footer:start]This opens the **Type Panel** where we can select one of the three Super Types to view their Concept Types.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1.1/visualise_types-select.png)[body:end]
[footer:start]We can then click on any of the Concept Types which may be an entity, an attribute or a relationship.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1.1/visualise_types-clicked.png)[body:end]
[footer:start]This constructs and inputs into the Graql Editor, a query that retrieves the concepts of the selected Type.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1.1/visualise_types-play.png)[body:end]
[footer:start]We can then click on the **execute** button to run the query.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1.1/visualise_types-response.png)[body:end]
[footer:start]And visualise its result.[footer:end]
[slide:end]

</div>

### Star Queries
<div class="slideshow">

[slide:start]
[body:start]![query in one line](/docs/images/workbase/1.1.1/visualise_star.png)[body:end]
[footer:start]To star the query written in the Graql Editor, we need to click on the **star** icon.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![query in one line](/docs/images/workbase/1.1.1/visualise_star-opened.png)[body:end]
[footer:start]This opens a form for starring the query.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1.1/visualise_star-name.png)[body:end]
[footer:start]Then we need to give the query a name and **save** it.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1.1/visualise_star-saved-queries-btn.png)[body:end]
[footer:start]To view the starred queries, we need to click on the **star** icon in the top bar.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1.1/visualise_star-saved-queries.png)[body:end]
[footer:start]This lists all starred queries.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1.1/visualise_star-use.png)[body:end]
[footer:start]We can choose to paste the query in the Graql Editor.[footer:end]
[slide:end]
<!-- -->
[slide:start]

[body:start]![Launch](/docs/images/workbase/1.1.1/visualise_star-used.png)[body:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1.1/visualise_star-edit.png)[body:end]
[footer:start]Or edit it.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1.1/visualise_star-editing.png)[body:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1.1/visualise_star-delete.png)[body:end]
[footer:start]Or delete it.[footer:end]
[slide:end]

</div>

### Access Query History
To navigate between Graql queries that we have previously executed, while in the Graql Editor, we need to _hold shift and press the up or down arrow key_.

### Configure Query Settings
<div class="slideshow">

[slide:start]
[body:start]![query in one line](/docs/images/workbase/1.1.1/visualise_query-settings.png)[body:end]
[footer:start]To configure query settings, click on the **gear** icon.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![query in one line](/docs/images/workbase/1.1.1/visualise_query-settings-tab.png)[body:end]
[footer:start]Expand the **Query Settings** section.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Graql editor](/docs/images/workbase/1.1.1/visualise_query-settings-query-limit.png)[body:end]
[footer:start]To avoid convoluting the visualiser, it's a good idea to limit the number of results return by a query. That's what the **Query Limit** is for.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Graql editor](/docs/images/workbase/1.1.1/visualise_query-settings-neighbour-limit.png)[body:end]
[footer:start]For the same reason, we may want to limit the number of neighbours to view when [investigating nodes](...). For this, we specify the **Neighbour Limit**.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Graql editor](/docs/images/workbase/1.1.1/visualise_query-settings-roleplayers.png)[body:end]
[footer:start]Lastly, we can choose to view or hide the roleplayers.[footer:end]
[slide:end]

</div>

### Visualise Multiple Queries
<div class="slideshow">

[slide:start]
[body:start]![tabs](/docs/images/workbase/1.1.1/visualise_tabs.png)[body:end]
[footer:start]To visualise multiple queries or keyspaces at the same time, we can create a new tab by clicking the **plus** icon on the bottom left.[footer:end]
[slide:end]

[slide:start]
[body:start]![tabs](/docs/images/workbase/1.1.1/visualise_tabs_new.png)[body:end]
[footer:start]Each tab will be mutually exclusive.[footer:end]
[slide:end]

[slide:start]
[body:start]![tabs](/docs/images/workbase/1.1.1/visualise_tabs_rename.png)[body:end]
[footer:start]We may also rename a tab by double clicking on the tab and then save it by clicking the **tick** icon.[footer:end]
[slide:end]

[slide:start]
[body:start]![tabs](/docs/images/workbase/1.1.1/visualise_tabs_close.png)[body:end]
[footer:start]We may close a tab by clicking the **cross** icon.[footer:end]
[slide:end]

</div>