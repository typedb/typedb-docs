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

