---
pageTitle: Grakn Workbase
keywords: grakn, workbase, visualiser, visualisation, visualizer, visualization
longTailKeywords: grakn workbase, grakn visualiser, grakn visualisation, grakn visualizer, grakn visualization
Summary: An overview of Grakn Workbase.
toc: false
---

## What is Workbase?
The Grakn Workbase, along with the [Grakn Console](../02-running-grakn/02-console.md) and the [Grakn Clients](../03-client-api/00-overview.md), is an interface through which we can read from a Grakn knowledge graph.
Workbase allows us to execute Graql [`get`](../10-query/02-get-query.md) and [`compute path`](../10-query/07-compute-query.md#compute-the-shortest-path) queries, and visualise and investigate their results.
Whether you need a tool to test and experiment with your newly created Grakn knowledge graph, or that you prefer a graphical interface for reading data from Grakn, you will find Workbase extremely useful.

<div class="note">
[Important]
Workbase is the newest member of the Grakn family of products and will undergo heavy development in years to come. At the moment, Workbase may only be used to _read_ data from a Grakn knowledge graph.
In the next release, Workbase will include the graphical interface for designing and visualising the schema. The future releases of Workbase are aimed at enabling write operations as well.
</div>

## Download Workbase
Grakn Workbase is available for Linux, Mac and Windows. Head over to the [Download Center](https://grakn.ai/download#workbase) to download and install the latest release of Workbase.

In the sections that follow, we learn how to [connect](../07-workbase/01-connection.md) Workbase with the Grakn Server, execute and [visusalise](../07-workbase/02-visualisation.md) queries, interact with the visualiser to [investigate](../07-workbase/03-investigation.md) the results and use the [schema designer](../07-workbase/04-schema-designer.md).