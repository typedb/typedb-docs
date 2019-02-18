---
sidebarTitle: Visualisation
pageTitle: Visualising Results
permalink: /docs/workbase/visualisation
toc: false
---

## Visualise
Workbase allows visualisation of answers returned by [Graql queries](/docs/query/overview). These include _custom_ and _pre-defined type-based_ queries.

### Execute Custom Queries
<div class="slideshow">

[slide:start]
[body:start]![Graql editor](/docs/images/workbase/1.1/custom_queries_1.png)[body:end]
[footer:start][Having selected the keyspace](/docs/workbase/preferences#selecting-a-keyspace), we can write queries of our own in the Graql Editor.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![query in one line](/docs/images/workbase/1.1/custom_queries_2.png)[body:end]
[footer:start]We can write queries in one single line.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1/custom_queries_3.png)[body:end]
[footer:start]Or in multiple lines by _holding shift and pressing enter_.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1/custom_queries_4.png)[body:end]
[footer:start]To run the query, we need to press the _execute_ button.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1/custom_queries_5.png)[body:end]
[footer:start]Executing a query visualises the result.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1/custom_queries_6.png)[body:end]
[footer:start]To clear the results, we need to click on the _refresh_ button.[footer:end]
[slide:end]
<!-- -->
[slide:start]

[body:start]![Launch](/docs/images/workbase/1.1/custom_queries_7.png)[body:end]
[footer:start]We can also minimise the Graql Editor to focus on the visualised results.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1/custom_queries_8.png)[body:end]
[footer:start]To clear the the Graql Editor, we need to click on the _delete_ button.[footer:end]
[slide:end]
</div>

### Execute Type-based Queries
<div class="slideshow">

[slide:start]
[body:start]![Graql editor](/docs/images/workbase/1.1/type_based_1.png)[body:end]
[footer:start][Having selected the keyspace](/docs/workbase/preferences#selecting-a-keyspace), we can explore the [Concept Types](/docs/schema/concepts) as defined in the [schema](/docs/schema/overview).[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![query in one line](/docs/images/workbase/1.1/type_based_2.png)[body:end]
[footer:start]This opens the _Types Panel_ where we can select one of the three Super Types to view their Concept Types.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1/type_based_3.png)[body:end]
[footer:start]We can then click on any of the Concept Types which may be an entity, an attribute or a relationship.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1/type_based_4.png)[body:end]
[footer:start]This constructs and inputs into the Graql Editor, a query that retrieves the concepts of the selected Type.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1/type_based_5.png)[body:end]
[footer:start]We can then click on the _execute_ button to run the query.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1/type_based_6.png)[body:end]
[footer:start]And visualise its result.[footer:end]
[slide:end]

</div>

### Star Queries
<div class="slideshow">

[slide:start]
[body:start]![query in one line](/docs/images/workbase/1.1/star_1.png)[body:end]
[footer:start]To star the query written in the Graql Editor, we need to click on the _star_ icon.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![query in one line](/docs/images/workbase/1.1/star_2.png)[body:end]
[footer:start]This opens a form for starring the query.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1/star_3.png)[body:end]
[footer:start]Then we need to give the query a name and _save_ it.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1/star_4.png)[body:end]
[footer:start]To view the starred queries, we need to click on the _star_ icon in the top bar.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1/star_5.png)[body:end]
[footer:start]This lists all starred queries.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1/star_6.png)[body:end]
[footer:start]We can choose to paste the query in the Graql Editor.[footer:end]
[slide:end]
<!-- -->
[slide:start]

[body:start]![Launch](/docs/images/workbase/1.1/star_7.png)[body:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1/star_8.png)[body:end]
[footer:start]Or edit it.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1/star_9.png)[body:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Launch](/docs/images/workbase/1.1/star_10.png)[body:end]
[footer:start]Or delete it.[footer:end]
[slide:end]

</div>

### Access Query History
To navigate between Graql queries that we have previously executed, while in the Graql Editor, we need to _hold shift and press the up or down arrow key_.

### Configure Query Settings
<div class="slideshow">

[slide:start]
[body:start]![query in one line](/docs/images/workbase/1.1/query_settings_1.png)[body:end]
[footer:start]To configure query settings, click on the _gear_ icon.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![query in one line](/docs/images/workbase/1.1/query_settings_2.png)[body:end]
[footer:start]Expand the _Query Settings_ section.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Graql editor](/docs/images/workbase/1.1/query_settings_3.png)[body:end]
[footer:start]To avoid convoluting the visualiser, it's a good idea to limit the number of results return by a query. That's what the _Query Limit_ is for.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Graql editor](/docs/images/workbase/1.1/query_settings_4.png)[body:end]
[footer:start]For the same reason, we may want to limit the number of neighbours to view when [investigating nodes](...). For this, we specify the _Neighbour Limit_.[footer:end]
[slide:end]
<!-- -->
[slide:start]
[body:start]![Graql editor](/docs/images/workbase/1.1/query_settings_5.png)[body:end]
[footer:start]Lastly, we can choose to view or hide the roleplayers.[footer:end]
[slide:end]

</div>

### Visualise Multiple Queries
<div class="slideshow">

[slide:start]
[body:start]![tabs](/docs/images/workbase/1.1/tabs_1.png)[body:end]
[footer:start]To visualise multiple queries or keyspaces at the same time, we can create a new tab by clicking the __plus__ icon on the bottom left.[footer:end]
[slide:end]

[slide:start]
[body:start]![tabs](/docs/images/workbase/1.1/tabs_2.png)[body:end]
[footer:start]Each tab will be mutually exclusive.[footer:end]
[slide:end]

[slide:start]
[body:start]![tabs](/docs/images/workbase/1.1/tabs_3.png)[body:end]
[footer:start]We may also rename a tab by double clicking on the tab and then save it by clicking the __tick__ icon.[footer:end]
[slide:end]

[slide:start]
[body:start]![tabs](/docs/images/workbase/1.1/tabs_4.png)[body:end]
[footer:start]We may close a tab by clicking the __cross__ icon.[footer:end]
[slide:end]

</div>