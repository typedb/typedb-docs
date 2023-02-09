---
pageTitle: Transactions
keywords: typedb, transactions
longTailKeywords: TypeDB transactions
summary: Description of TypeDB transactions.
toc: false
---

A transaction performs queries on the database. TypeDB transactions comply with
[ACID](03-acid.md) properties, up to snapshot isolation.

Transactions automatically close after a set timeout period (default value is 5 minutes, but it can be changed with 
[client](04-clients.md) options). This is to encourage shorter-lived transactions, prevent memory leaks caused by 
forgotten unclosed client-side transactions, and kill potentially unresponsive transactions.

## Best Practices

Keep transactions generally short-lived. Long-lived transactions are more likely to clash with others when committing, 
and pin resources in the server.

A good principle is that transactions group logically coherent queries. For example, when building an e-commerce 
platform, loading a user's purchase history page could be done using two transactions: one for retrieving the purchases, 
and another for retrieving the user's profile.

However, when leveraging the TypeDB reasoning engine, it is sometimes beneficial to reuse the same read transactions to 
warm up the reasoning caches.
