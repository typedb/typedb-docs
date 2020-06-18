---
pageTitle: Grakn Workbase
keywords: grakn, workbase, visualiser, visualisation, visualizer, visualization
longTailKeywords: grakn workbase, grakn visualiser, grakn visualisation, grakn visualizer, grakn visualization
Summary: An overview of Grakn Workbase.
toc: false
---

## What is Workbase?
The Grakn Workbase, along with the [Grakn Console](../02-running-grakn/02-console.md) and the [Grakn Clients](../03-client-api/00-overview.md), is an interface through which we can read from a Grakn knowledge graph.
Workbase allows us to execute Graql [`get`](../11-query/02-get-query.md) and [`compute path`](../11-query/07-compute-query.md#compute-the-shortest-path) queries, and visualise and investigate their results.
Whether you need a tool to test and experiment with your newly created Grakn knowledge graph, or that you prefer a graphical interface for reading data from Grakn, you will find Workbase extremely useful.

## Download Workbase
Grakn Workbase is available for Linux, Mac and Windows. Head over to the [Download Center](https://grakn.ai/download#workbase) to download and install the latest release of Workbase.

<div class="note">
[Important]
As of Grakn 1.6.0, _explanations_ of inferred concepts can behave unexpectedly. Explanations of inferred relations will not show source relations in the visualiser, if the rule `when` clause that produced the relation is not tagged with a variable. For example:

<!-- test-ignore -->
```graql
when { (less: $x, more: $y) isa greater-than; (less: $y, more: $z) isa greater-than; },
then { (less: $x, more: $z) isa greater-than; };
```

Asking workbase to explain inferred transitive `($x, $z)` relations does not produce the source relations, unless labeling them with some other variables:

<!-- test-ignore -->
```graql
when { $r1 (less: $x, more: $y) isa greater-than; $r2 (less: $y, more: $z) isa greater-than; },
then { (less: $x, more: $z) isa greater-than; };
```
  
  Note that this can have a performance impact, so in production we recommend only leaving the relation variables as required.
</div>

## Dependencies

| Workbase       | Grakn Core          | Grakn KGMS          |
| :------------: | :-----------------: | :-----------------: |
| 1.3.0          | 1.8.0               | N/A                 |
| 1.2.10         | 1.7.0 to 1.7.2      | N/A                 |
| 1.2.9          | 1.7.0 to 1.7.2      | N/A                 |
| 1.2.8          | 1.7.0 to 1.7.2      | N/A                 |
| 1.2.7          | 1.6.1, 1.6.2        | 1.6.2               |
| 1.2.6          | 1.5.9               | N/A                 |
| 1.2.5          | 1.5.9               | 1.5.8               |
| 1.2.4          | 1.5.9               | 1.5.8               |
| 1.2.3          | 1.5.8, 1.5.9        | 1.5.8               |
| 1.2.2          | 1.5.3 to 1.5.7      | 1.5.2 to 1.5.7      |
| 1.2.1          | 1.5.2               | 1.5.2               |
| 1.2.0          | 1.5.0, 1.5.1        | N/A                 |
| 1.0.0 to 1.1.1 | 1.4.0 to 1.4.3      | 1.4.0 to 1.4.3      |


In the sections that follow, we learn how to [connect](../07-workbase/01-connection.md) Workbase with the Grakn Server, execute and [visualise](../07-workbase/02-visualisation.md) queries, interact with the visualiser to [investigate](../07-workbase/03-investigation.md) the results and use the [schema designer](../07-workbase/04-schema-designer.md).
