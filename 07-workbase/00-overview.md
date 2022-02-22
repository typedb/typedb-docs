---
pageTitle: TypeDB Workbase
keywords: typeql, workbase, visualiser, visualisation, visualizer, visualization
longTailKeywords: typeql workbase, typeql visualiser, typeql visualisation, typeql visualizer, typeql visualization
Summary: An overview of TypeDB Workbase.
toc: false
---

<div class = "note">
[Warning]
TypeDB Workbase is currently in the process of being replaced with a more performant application: TypeDB Studio, which will be released very soon (March 2022)!
</div>

## What is Workbase?
The TypeDB Workbase, along with the [TypeDB Console](../02-console/01-console.md) and the [TypeDB Clients](../03-client-api/00-overview.md), is an interface through which we can read from a TypeDB knowledge graph.
Workbase allows us to execute TypeQL [`match`](../11-query/01-match-clause.md) queries, and visualise and investigate their results.
Whether you need a tool to test and experiment with your newly created TypeDB knowledge graph, or that you prefer a graphical interface for reading data from TypeDB, you will find Workbase extremely useful.

## Download Workbase
TypeDB Workbase is available for Linux, Mac and Windows. Head over to the [Download Center](https://vaticle.com/download#typedb-studio) to download and install the latest release of Workbase.


## Version Compatibility

| Workbase       | TypeDB          | TypeDB Cluster |
| :------------: | :-------------: | :------------: |
| 2.1.2          | 2.1.2 to 2.3.3  | 2.1.2 to 2.3.0 |
| 2.1.0          | 2.1.0           | 2.1.0          |
| 2.0.2          | 2.0.2           | 2.0.2          |
| 2.0.0, 2.0.1   | 2.0.0, 2.0.1    | 2.0.0, 2.0.1   |
| 1.3.5          | 1.8.0           | N/A            |
| 1.3.4          | 1.8.0           | N/A            |
| 1.3.3          | 1.8.0           | N/A            |
| 1.3.2          | 1.8.0           | N/A            |
| 1.3.1          | 1.8.0           | N/A            |
| 1.3.0          | 1.8.0           | N/A            |


In the sections that follow, we learn how to [connect](../07-workbase/01-connection.md) Workbase with the TypeDB Server, execute and [visualise](../07-workbase/02-visualisation.md) queries, interact with the visualiser to [investigate](../07-workbase/03-investigation.md) the results and use the [schema designer](../07-workbase/04-schema-designer.md).
