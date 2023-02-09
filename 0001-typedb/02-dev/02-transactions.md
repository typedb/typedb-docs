---
pageTitle: Transactions
keywords: typedb, transactions
longTailKeywords: TypeDB transactions
summary: Description of TypeDB transactions.
toc: false
---

# Transactions

All queries to a TypeDB database are performed through transactions.
TypeDB provides [ACID](03-acid.md) guarantees, up to [snapshot isolation](03-acid.md#isolation), through of schema 
validation and consistent transactions.

All transactions to TypeDB must be explicit — deliberately opened and closed. TypeDB Studio can manage transactions 
for you but other clients provide instruments for explicit transaction control.

There are two types of transactions in TypeDB:

- Read
- Write

TypeDB has lightweight optimistic transactions: it allows a high number of concurrent read and write transactions. 

Transactions in TypeDB have atomic all-or-nothing commits, which makes transactional semantics become easy to reason 
over. If transaction is failed for any reason the changes will not be persisted.

Successful write transaction commit gets written to write-ahead-log (or WAL file) before TypeDB sends 
confirmation of successful transaction (see [Durability guarantees](03-acid.md#durability)).

Unsuccessful write transaction gets closed without persisting any changes.

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
