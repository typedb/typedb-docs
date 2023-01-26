---
pageTitle: Session
keywords: typedb, session
longTailKeywords: typedb session
summary: TypeDB session concept.
toc: false
---

<!--- 
A grouping of transactions, access either schema or data - schema is “admin” type and prevents data write transactions opening, can be opened with session-wide options.
-->

# Session

A session holds a connection to a particular database. This connection then allows opening [transactions](05-transaction.md) to carry out [queries](06-query.md). 

## Best Practices

Because of intermittent network failures, it is recommended to keep sessions relatively short-lived.

A good principle is that sessions group logically coherent transactions. For example, when loading a web page, one 
session should be used to open one or more transactions to load the page data.

