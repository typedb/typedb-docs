---
pageTitle: Query
keywords: typedb, query
longTailKeywords: typedb query
summary: TypeDB query concept.
toc: false
---

<!--- 
All TypeDB queries are via TypeQL. Queries within a transaction. Queries either return a single answer/answer group, or are lazily streamed back. Writes are always eager, but return values are lazy. Lazy streams are reactive - computation proceeds as requested with some amount of precomputation. Queries are also async, so can be interleaved. Concurrent queries that interact via writes do not produce well-defined outcomes. Can be run with query-level options (also inherits txn & session options)
-->

# Query

Queries are prepared in [TypeQL](../../11-query/00-overview.md) query language for the TypeDB knowledge graph. Whether 
it's through the [TypeDB Console](../02-console/01-console.md), [TypeDB Studio](../07-studio/00-overview.md) or one of 
the [TypeDB Clients](../03-client-api/00-overview.md), TypeDB accepts instructions and provides answers only in its own 
language - TypeQL.

### Async Queries
Invoking a TypeQL query sends the query to the TypeDB server, where it will be completed in the background. Local processing can take place while waiting for responses to be received. Take advantage of these asynchronous queries to mask network round-trip costs and increases your throughput. For example, if you are performing 10 match queries in a transaction, it's best to send them all to the server _before_ iterating over any of their answers.

Queries that return answers, such as [match](../../11-query/01-match-clause.md), return them as Futures, Streams or 
Iterators depending on the language. These can then be awaited, or iterated, to retrieve the answers as they are computed.

<div class="note">
[Important]
When a transaction is committed or closed, all of its asynchronous queries are completed first.
</div>

### Investigating Answers
Depending on the type of the query carried out by a transaction, we retrieve different forms of answers. These answers, regardless of their type, all contain concepts. We can then use the methods introduced by the 
[Concept API](../../04-concept-api/00-overview.md) to obtain more information about the retrieved concept and its surroundings. Furthermore, the Concept API allows us to traverse the neighbours of a specific concept instance to obtain more insights.


