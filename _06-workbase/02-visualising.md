---
title: Visualising
keywords:
tags: []
summary: ""
permalink: /docs/workbase/visualising
---

## Visualise
Workbase allows visualisation of answers returned by [Graql queries](/docs/query/overview). These include _custom_ and _pre-defined type-based_ queries.

<div class="galert">
[Important]
For the purpose of demonstration, we will be interacting with the `phone_calls` keyspace. If you'd like to follow the instructions below step-by-step and see the results accordingly, you need to have modeled the `phone_calls` knowledge graph, loaded its schema into a keyspace and migrated the dataset into it. To do so, follow the [Phone Calls Example](...).
</div>

### Execute Custom Queries
<div class="slideshow">

[slide:start]
[body:start]![Graql editor](/docs/images/workbase/main_graql-editor.png)[body:end]
[footer:start][Having selected the keyspace](/docs/workbase/preferences#selecting-a-keyspace), we can write queries of our own in the Graql Editor.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![query in one line](/docs/images/workbase/graql-editor_singleline.png)[body:end]
[footer:start]We can write queries in one single line.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/graql-editor_multiline.png)[body:end]
[footer:start]Or in multiple lines by _holding shift and pressing enter_.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/graql-editor_execute.png)[body:end]
[footer:start]To run the query, we need to press the _execute_ button.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/graql-editor_executed.png)[body:end]
[footer:start]Executing a query visualises the result.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/graql-editor_clear-graph.png)[body:end]
[footer:start]To clear the results, we need to click on the _refresh_ button.[footer:end]
[slide:end]
<!-- -->
[slide:start]

[body:start]![Launch](/docs/images/workbase/graql-editor_minimise.png)[body:end]
[footer:start]We can also minimise the Graql Editor to focus on the visualised results.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/graql-editor_clear-query.png)[body:end]
[footer:start]To clear the the Graql Editor, we need to click on the _delete_ button.[footer:end]
[slide:end]
</div>

### Execute Type-based Queries
<div class="slideshow">

[slide:start]
[body:start]![Graql editor](/docs/images/workbase/main_types.png)[body:end]
[footer:start][Having selected the keyspace](/docs/workbase/preferences#selecting-a-keyspace), we can explore the [Concept Types](/docs/schema/concepts) as defined in the [schema](/docs/schema/overview).[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![query in one line](/docs/images/workbase/types.png)[body:end]
[footer:start]This opens the _Types Panel_ where we can select one of the three Super Types to view their Concept Types.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/types_select.png)[body:end]
[footer:start]We can then click on any of the Concept Types which may be an entity, an attribute or a relationship.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/types_selected.png)[body:end]
[footer:start]This constructs and inputs into the Graql Editor, a query that retrieves the concepts of the selected Type.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/types_execute.png)[body:end]
[footer:start]We can then click on the _execute_ button to run the query.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/types_executed.png)[body:end]
[footer:start]And visualise its result.[footer:end]
[slide:end]

</div>

### Star Queries
<div class="slideshow">

[slide:start]
[body:start]![query in one line](/docs/images/workbase/graql-editor_star.png)[body:end]
[footer:start]To star the query written in the Graql Editor, we need to click on the _star_ icon.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![query in one line](/docs/images/workbase/graql-editor_star-form_blank.png)[body:end]
[footer:start]This opens a form for starring the query.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/graql-editor_star-form_filled.png)[body:end]
[footer:start]Then we need to give the query a name and _save_ it.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/main_starred-queries.png)[body:end]
[footer:start]To view the starred queries, we need to click on the _star_ icon in the top bar.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/starred-queries.png)[body:end]
[footer:start]This will list all starred queries.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/starred-queries_input.png)[body:end]
[footer:start]We can choose to paste the query in the Graql Editor.[footer:end]
[slide:end]
<!-- -->
[slide:start]

[body:start]![Launch](/docs/images/workbase/starred-queries_inputted.png)[body:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/starred-queries_edit.png)[body:end]
[footer:start]Or edit it.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/starred-queries_edit-form.png)[body:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/starred-queries_delete.png)[body:end]
[footer:start]Or delete it.[footer:end]
[slide:end]

</div>

### Access Query History
To navigate between Graql queries that we have previously executed, while in the Graql Editor, we need to _hold shift and press the up or down arrow key_.

### Configure Query Settings
<div class="slideshow">

[slide:start]
[body:start]![query in one line](/docs/images/workbase/main_settings.png)[body:end]
[footer:start]To configure query settings, click on the _gear_ icon.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![query in one line](/docs/images/workbase/settings_query.png)[body:end]
[footer:start]Expand the _Query Settings_ section.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Graql editor](/docs/images/workbase/settings_query_limit.png)[body:end]
[footer:start]To avoid convoluting the visualiser, it's a good idea to limit the number of results return by a query. That's what the _Query Limit_ is for.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Graql editor](/docs/images/workbase/settings_query_neighbour-limit.png)[body:end]
[footer:start]For the same reason, we may want to limit the number of neighbours to view when [investigating nodes](...). For this, we specify the _Neighbour Limit_.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Graql editor](/docs/images/workbase/settings_query_roleplayers.png)[body:end]
[footer:start]Lastly, we can choose to view or hide the roleplayers.[footer:end]
[slide:end]

</div>